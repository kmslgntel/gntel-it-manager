"""
migrate_legacy — .sql 백업 파일을 파싱해 신규 DB로 데이터 이전

사용법:
  python manage.py migrate_legacy --sql-file 20260528_sqlbackup.sql
  python manage.py migrate_legacy --sql-file 20260528_sqlbackup.sql --dry-run
  python manage.py migrate_legacy --sql-file 20260528_sqlbackup.sql --table CPY_INF
"""

import re
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# 이전 대상 외 무시할 테이블
SKIP_TABLES = {
    'IP_MNG_TEST', 'IP_MNG_LOG_TEST', 'PHN_MNG_tmp',
    'USR_INF_250103', 'USR_INF_TMP', 'ip_mng_backup',
    'switch_config_backup', 'IP_MNG_LOG', 'CHANGE_LOG',
}


# ─────────────────────────────────────────────
# SQL 파싱 유틸
# ─────────────────────────────────────────────

def parse_sql_file(sql_path):
    """
    .sql 파일에서 INSERT IGNORE INTO 구문을 테이블별로 수집.
    반환: {table_name: [(col_list, values_list), ...]}
    """
    result = {}
    with open(sql_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 주석 제거 (-- ... 및 /* ... */)
    content = re.sub(r'--[^\n]*', '', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    pattern = re.compile(
        r"INSERT\s+IGNORE\s+INTO\s+`?(\w+)`?\s*"
        r"\(([^)]+)\)\s*VALUES\s*(.+?);\s*",
        re.IGNORECASE | re.DOTALL,
    )

    for m in pattern.finditer(content):
        table = m.group(1)
        cols_raw = m.group(2)
        vals_raw = m.group(3)

        cols = [c.strip().strip('`') for c in cols_raw.split(',')]
        rows = _parse_rows(vals_raw)

        if table not in result:
            result[table] = []
        result[table].append((cols, rows))

    return result


def _parse_rows(vals_raw):
    """VALUES 절에서 row 튜플 목록 파싱 — 중첩 괄호/문자열 처리"""
    rows = []
    i = 0
    n = len(vals_raw)
    while i < n:
        if vals_raw[i] == '(':
            row, i = _parse_single_row(vals_raw, i + 1)
            rows.append(row)
        else:
            i += 1
    return rows


def _parse_single_row(s, start):
    """단일 행의 값 목록 파싱, 파싱 종료 위치 반환"""
    values = []
    current = []
    i = start
    in_string = False
    n = len(s)

    while i < n:
        c = s[i]
        if in_string:
            if c == '\\' and i + 1 < n:
                current.append(c)
                i += 1
                current.append(s[i])
            elif c == "'":
                current.append(c)
                in_string = False
            else:
                current.append(c)
        else:
            if c == "'":
                current.append(c)
                in_string = True
            elif c == ',':
                values.append(_normalize_value(''.join(current).strip()))
                current = []
            elif c == ')':
                values.append(_normalize_value(''.join(current).strip()))
                return values, i + 1
            else:
                current.append(c)
        i += 1

    values.append(_normalize_value(''.join(current).strip()))
    return values, i


def _normalize_value(raw):
    """raw 문자열을 Python 값으로 변환"""
    if raw.upper() == 'NULL':
        return None
    if raw.startswith("'") and raw.endswith("'"):
        inner = raw[1:-1]
        # MySQL 이스케이프 처리
        inner = inner.replace("\\'", "'").replace('\\\\', '\\')
        inner = inner.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')
        return inner
    # 숫자
    try:
        if '.' in raw:
            return float(raw)
        return int(raw)
    except (ValueError, TypeError):
        return raw


def rows_to_dicts(cols, rows):
    """열 이름과 행 목록을 dict 목록으로 변환"""
    return [dict(zip(cols, row)) for row in rows]


# ─────────────────────────────────────────────
# 모델별 이전 함수
# ─────────────────────────────────────────────

def migrate_companies(data, dry_run, stdout):
    from assets.models import Company
    rows = _collect_rows(data, 'CPY_INF')
    created = updated = 0
    for r in rows:
        cocd = str(r.get('COCD', '') or '').strip()
        name = str(r.get('CPY_NAME', '') or '').strip()
        if not cocd:
            continue
        if not dry_run:
            _, is_new = Company.objects.update_or_create(
                code=cocd, defaults={'name': name}
            )
        else:
            is_new = not Company.objects.filter(code=cocd).exists()
        if is_new:
            created += 1
        else:
            updated += 1
    stdout.write(f"  Company: 신규 {created}, 갱신 {updated}")


def migrate_departments(data, dry_run, stdout):
    from assets.models import Company, Department
    rows = _collect_rows(data, 'DPT_INF')
    created = updated = skipped = 0
    for r in rows:
        code = str(r.get('DEPT_CODE', '') or '').strip()
        if not code:
            continue
        cocd = str(r.get('COCD', '') or '').strip()
        company = Company.objects.filter(code=cocd).first() if cocd else None
        defaults = {
            'name': str(r.get('DEPT_NAME', '') or ''),
            'name_en': str(r.get('DEPT_NAME_EN', '') or ''),
            'high_dept_code': str(r.get('HIGH_DEPT_CODE', '') or ''),
            'use_yn': str(r.get('USEYN', '') or 'Y')[:1] or 'Y',
            'company': company,
        }
        step = r.get('STEP')
        if step is not None:
            try:
                defaults['step'] = int(step)
            except (ValueError, TypeError):
                pass
        vo = r.get('VIEW_ORDER')
        if vo is not None:
            try:
                defaults['view_order'] = int(vo)
            except (ValueError, TypeError):
                pass
        if not dry_run:
            _, is_new = Department.objects.update_or_create(code=code, defaults=defaults)
        else:
            is_new = not Department.objects.filter(code=code).exists()
        if is_new:
            created += 1
        else:
            updated += 1
    stdout.write(f"  Department: 신규 {created}, 갱신 {updated}")


def migrate_persons(data, dry_run, stdout):
    from assets.models import Company, Department, Person

    # USR_INF → employee
    emp_rows = _collect_rows(data, 'USR_INF')
    created = updated = 0
    for r in emp_rows:
        uid = str(r.get('USER_ID', '') or '').strip()
        if not uid:
            continue
        dept = Department.objects.filter(code=str(r.get('DEPT_CODE', '') or '')).first()
        cocd = str(r.get('COCD', '') or '').strip()
        company = Company.objects.filter(code=cocd).first() if cocd else None
        defaults = {
            'name': str(r.get('USER_NAME', '') or ''),
            'name_en': str(r.get('USER_NAME_EN', '') or ''),
            'department': dept,
            'company': company,
            'grade': str(r.get('GRADE_NM', '') or ''),
            'emp_no': str(r.get('EMP_NO', '') or ''),
            'email': str(r.get('EMAIL', '') or ''),
            'tel': str(r.get('TEL', '') or ''),
            'hp': str(r.get('HP', '') or ''),
            'use_yn': str(r.get('USE_YN', '') or 'Y')[:1] or 'Y',
            'resign_dt': str(r.get('RESIGN_DT', '') or ''),
        }
        if not dry_run:
            _, is_new = Person.objects.update_or_create(
                person_type='employee', legacy_id=uid, defaults=defaults
            )
        else:
            is_new = not Person.objects.filter(person_type='employee', legacy_id=uid).exists()
        if is_new:
            created += 1
        else:
            updated += 1
    stdout.write(f"  Person(employee): 신규 {created}, 갱신 {updated}")

    # OTH_INF → other  (get_or_create 만 — 수동 생성 데이터 보호)
    oth_rows = _collect_rows(data, 'OTH_INF')
    o_created = o_skip = 0
    for r in oth_rows:
        oid = str(r.get('OTHER_ID', '') or '').strip()
        if not oid:
            continue
        if not dry_run:
            dept = Department.objects.filter(code=str(r.get('DEPT_CODE', '') or '')).first()
            cocd = str(r.get('COCD', '') or '').strip()
            company = Company.objects.filter(code=cocd).first() if cocd else None
            _, is_new = Person.objects.get_or_create(
                person_type='other', legacy_id=oid,
                defaults={
                    'name': str(r.get('OTHER_NAME', '') or ''),
                    'department': dept,
                    'company': company,
                    'use_yn': str(r.get('USE_YN', '') or 'Y')[:1] or 'Y',
                }
            )
            if is_new:
                o_created += 1
            else:
                o_skip += 1
        else:
            if not Person.objects.filter(person_type='other', legacy_id=oid).exists():
                o_created += 1
            else:
                o_skip += 1
    stdout.write(f"  Person(other): 신규 {o_created}, 기존 유지 {o_skip}")


def migrate_ip_groups(data, dry_run, stdout):
    from assets.models import IpGroup

    # IP_PRN_INF 로 parent_name 매핑 구성
    prn_map = {}
    for r in _collect_rows(data, 'IP_PRN_INF'):
        pid = str(r.get('PARENT_ID', '') or '').strip()
        pname = str(r.get('PARENT_NAME', '') or '').strip()
        if pid:
            prn_map[pid] = pname

    created = updated = 0
    # IP_GRP_INF
    for r in _collect_rows(data, 'IP_GRP_INF'):
        gid = str(r.get('GROUP_ID', '') or '').strip()
        if not gid:
            continue
        parent_id = str(r.get('PARENT_ID', '') or '').strip()
        defaults = {
            'name': str(r.get('GROUP_NAME', '') or ''),
            'parent_name': prn_map.get(parent_id, ''),
            'is_phone_group': False,
        }
        if not dry_run:
            _, is_new = IpGroup.objects.update_or_create(
                legacy_group_id=gid, is_phone_group=False, defaults=defaults
            )
        else:
            is_new = not IpGroup.objects.filter(legacy_group_id=gid, is_phone_group=False).exists()
        if is_new:
            created += 1
        else:
            updated += 1

    # GRP_INF (전화기 IP 그룹)
    for r in _collect_rows(data, 'GRP_INF'):
        gid = str(r.get('GROUP_ID', '') or '').strip()
        if not gid:
            continue
        defaults = {
            'name': str(r.get('GROUP_NAME', '') or ''),
            'parent_name': '',
            'is_phone_group': True,
        }
        if not dry_run:
            _, is_new = IpGroup.objects.update_or_create(
                legacy_group_id=gid, is_phone_group=True, defaults=defaults
            )
        else:
            is_new = not IpGroup.objects.filter(legacy_group_id=gid, is_phone_group=True).exists()
        if is_new:
            created += 1
        else:
            updated += 1

    stdout.write(f"  IpGroup: 신규 {created}, 갱신 {updated}")


def migrate_ip_addresses(data, dry_run, stdout):
    from assets.models import IpAddress, IpGroup, Person

    rows = _collect_rows(data, 'IP_MNG')
    created = updated = 0

    for r in rows:
        ip_id_raw = str(r.get('IP_ID', '') or '').strip()
        ip_str = str(r.get('IP', '') or '').strip()
        if not ip_str or not ip_id_raw:
            continue
        try:
            ip_int = int(ip_id_raw)
        except ValueError:
            continue

        gid = str(r.get('GROUP_ID', '') or '').strip()
        group = IpGroup.objects.filter(legacy_group_id=gid, is_phone_group=False).first() if gid else None
        uid = str(r.get('USER_ID', '') or '').strip()
        person = None
        if uid:
            person = (Person.objects.filter(person_type='employee', legacy_id=uid).first()
                      or Person.objects.filter(person_type='other', legacy_id=uid).first())

        defaults = {
            'ip': ip_str,
            'group': group,
            'person': person,
            'note': str(r.get('NOTE', '') or ''),
            'start_date': str(r.get('START_DATE', '') or ''),
            'end_date': str(r.get('END_DATE', '') or ''),
        }
        if not dry_run:
            _, is_new = IpAddress.objects.update_or_create(ip_int=ip_int, defaults=defaults)
        else:
            is_new = not IpAddress.objects.filter(ip_int=ip_int).exists()
        if is_new:
            created += 1
        else:
            updated += 1
    stdout.write(f"  IpAddress: 신규 {created}, 갱신 {updated}")


def migrate_network_devices(data, dry_run, stdout):
    from assets.models import IpAddress, NetworkDevice

    rows = _collect_rows(data, 'NTWR_DVCS_INF')
    created = updated = 0

    for r in rows:
        ip_id_raw = str(r.get('IP_ID', '') or '').strip()
        ip_str = str(r.get('IP', '') or '').strip()
        mac = str(r.get('MAC', '') or '').strip()

        ip_addr = None
        if ip_id_raw:
            try:
                ip_addr = IpAddress.objects.filter(ip_int=int(ip_id_raw)).first()
            except ValueError:
                pass

        defaults = {
            'ip_address': ip_addr,
            'ip': ip_str,
            'hostname': _euckr_fix(str(r.get('HNAME', '') or '')),
            'division': _euckr_fix(str(r.get('DIVISION', '') or '')),
            'scan_user': _euckr_fix(str(r.get('USER', '') or '')),
            'note': str(r.get('NOTE', '') or ''),
        }
        if not dry_run:
            if mac:
                _, is_new = NetworkDevice.objects.update_or_create(mac=mac, defaults=defaults)
            else:
                NetworkDevice.objects.create(**defaults)
                is_new = True
        else:
            is_new = not (mac and NetworkDevice.objects.filter(mac=mac).exists())
        if is_new:
            created += 1
        else:
            updated += 1
    stdout.write(f"  NetworkDevice: 신규 {created}, 갱신 {updated}")


def migrate_phones(data, dry_run, stdout):
    from assets.models import IpAddress, Person, Phone

    rows = _collect_rows(data, 'PHN_MNG')
    created = updated = 0

    for r in rows:
        pid = str(r.get('PHONE_ID', '') or '').strip()
        if not pid:
            continue
        uid = str(r.get('USER_ID', '') or '').strip()
        person = None
        if uid:
            person = (Person.objects.filter(person_type='employee', legacy_id=uid).first()
                      or Person.objects.filter(person_type='other', legacy_id=uid).first())
        ip_id_raw = str(r.get('IP_ID', '') or '').strip()
        ip_addr = None
        if ip_id_raw:
            try:
                ip_addr = IpAddress.objects.filter(ip_int=int(ip_id_raw)).first()
            except ValueError:
                pass
        defaults = {
            'person': person,
            'ip_address': ip_addr,
            'purpose': str(r.get('PURPOSE', '') or ''),
            'note': str(r.get('NOTE', '') or ''),
            'start_date': str(r.get('START_DATE', '') or ''),
            'end_date': str(r.get('END_DATE', '') or ''),
        }
        if not dry_run:
            _, is_new = Phone.objects.update_or_create(phone_id=pid, defaults=defaults)
        else:
            is_new = not Phone.objects.filter(phone_id=pid).exists()
        if is_new:
            created += 1
        else:
            updated += 1
    stdout.write(f"  Phone: 신규 {created}, 갱신 {updated}")


def migrate_racks(data, dry_run, stdout):
    from switches.models import Rack
    rows = _collect_rows(data, 'RCK_INF')
    created = updated = 0
    for r in rows:
        rid = r.get('RACK_ID')
        if rid is None:
            continue
        try:
            rid = int(rid)
        except (ValueError, TypeError):
            continue
        defaults = {'name': str(r.get('RACK_NAME', '') or '')}
        if not dry_run:
            _, is_new = Rack.objects.update_or_create(legacy_rack_id=rid, defaults=defaults)
        else:
            is_new = not Rack.objects.filter(legacy_rack_id=rid).exists()
        if is_new:
            created += 1
        else:
            updated += 1
    stdout.write(f"  Rack: 신규 {created}, 갱신 {updated}")


def migrate_switches(data, dry_run, stdout):
    from switches.models import Rack, Switch
    rows = _collect_rows(data, 'SWT_INF')
    created = updated = 0
    for r in rows:
        sid = r.get('SWITCH_ID')
        if sid is None:
            continue
        try:
            sid = int(sid)
        except (ValueError, TypeError):
            continue
        rid = r.get('RACK_ID')
        rack = None
        if rid is not None:
            try:
                rack = Rack.objects.filter(legacy_rack_id=int(rid)).first()
            except (ValueError, TypeError):
                pass
        ip_str = str(r.get('SWITCH_IP', '') or '').strip()
        if not ip_str:
            continue
        sort = r.get('SWITCH_SORT', 0)
        try:
            sort = int(sort)
        except (ValueError, TypeError):
            sort = 0
        defaults = {'rack': rack, 'ip': ip_str, 'sort_order': sort}
        if not dry_run:
            _, is_new = Switch.objects.update_or_create(legacy_switch_id=sid, defaults=defaults)
        else:
            is_new = not Switch.objects.filter(legacy_switch_id=sid).exists()
        if is_new:
            created += 1
        else:
            updated += 1
    stdout.write(f"  Switch: 신규 {created}, 갱신 {updated}")


def migrate_switch_ports(data, dry_run, stdout):
    from switches.models import Switch, SwitchPort

    # port_mode: SWT_PRT_MD_INF
    mode_map = {}
    for r in _collect_rows(data, 'SWT_PRT_MD_INF'):
        sid = r.get('SWITCH_ID')
        iface = str(r.get('INTERFACE', '') or '').strip()
        mode = str(r.get('PORT_MODE', '') or '').strip()
        if sid and iface:
            mode_map[(str(sid), iface)] = mode

    # location: PRT_CNC_LCT_INF
    loc_map = {}
    for r in _collect_rows(data, 'PRT_CNC_LCT_INF'):
        sid = r.get('SWITCH_ID')
        iface = str(r.get('INTERFACE', '') or '').strip()
        if sid and iface:
            loc_map[(str(sid), iface)] = {
                'area_number': str(r.get('AREA_NUMBER', '') or ''),
                'port_number': str(r.get('PORT_NUMBER', '') or ''),
            }

    # 모든 interface 합집합
    all_keys = set(mode_map.keys()) | set(loc_map.keys())
    created = updated = 0

    for sid_str, iface in all_keys:
        try:
            switch = Switch.objects.filter(legacy_switch_id=int(sid_str)).first()
        except (ValueError, TypeError):
            continue
        if not switch:
            continue
        defaults = {
            'port_mode': mode_map.get((sid_str, iface), ''),
            'area_number': loc_map.get((sid_str, iface), {}).get('area_number', ''),
            'port_number': loc_map.get((sid_str, iface), {}).get('port_number', ''),
        }
        if not dry_run:
            _, is_new = SwitchPort.objects.update_or_create(
                switch=switch, interface=iface, defaults=defaults
            )
        else:
            is_new = not SwitchPort.objects.filter(switch=switch, interface=iface).exists()
        if is_new:
            created += 1
        else:
            updated += 1
    stdout.write(f"  SwitchPort: 신규 {created}, 갱신 {updated}")


def migrate_switch_mac_entries(data, dry_run, stdout):
    from switches.models import Switch, SwitchMacEntry

    rows = _collect_rows(data, 'ETH_SWT_INF')
    if not dry_run:
        # MAC 정보는 갱신 시 전체 교체 방식 (원본도 replace 방식)
        sw_ids = {str(r.get('SWITCH_ID')) for r in rows if r.get('SWITCH_ID')}
        for sid_str in sw_ids:
            try:
                sw = Switch.objects.filter(legacy_switch_id=int(sid_str)).first()
                if sw:
                    sw.mac_entries.all().delete()
            except (ValueError, TypeError):
                pass

    created = 0
    for r in rows:
        sid = r.get('SWITCH_ID')
        iface = str(r.get('INTERFACE', '') or '').strip()
        mac = str(r.get('MAC', '') or '').strip()
        if not sid or not iface or not mac:
            continue
        try:
            switch = Switch.objects.filter(legacy_switch_id=int(sid)).first()
        except (ValueError, TypeError):
            continue
        if not switch:
            continue
        if not dry_run:
            SwitchMacEntry.objects.create(
                switch=switch,
                interface=iface,
                vlan=str(r.get('VLAN', '') or ''),
                mac=mac,
                entry_type=str(r.get('ENTRY_TYPE', '') or ''),
                age=str(r.get('AGE', '') or ''),
            )
        created += 1
    stdout.write(f"  SwitchMacEntry: {created}건 처리")


def migrate_switch_backups(data, dry_run, stdout):
    from switches.models import Switch, SwitchConfigBackup

    # SWT_BCK_INF: backup_id → date/time 매핑
    bck_inf_map = {}
    for r in _collect_rows(data, 'SWT_BCK_INF'):
        bid = str(r.get('BACKUP_ID', '') or '').strip()
        if bid:
            bck_inf_map[bid] = {
                'backup_date': str(r.get('BACKUP_DATE', '') or ''),
                'backup_time': str(r.get('BACKUP_TIME', '') or ''),
            }

    rows = _collect_rows(data, 'SWT_CNF_BCK')
    created = 0
    for r in rows:
        sid = r.get('SWITCH_ID')
        bid = str(r.get('BACKUP_ID', '') or '').strip()
        if not sid:
            continue
        try:
            switch = Switch.objects.filter(legacy_switch_id=int(sid)).first()
        except (ValueError, TypeError):
            continue
        if not switch:
            continue
        date_info = bck_inf_map.get(bid, {})
        backup_date = date_info.get('backup_date', '')
        backup_time = date_info.get('backup_time', '')

        # 동일 switch+date+time 이면 skip (멱등성)
        if not dry_run:
            if backup_date and backup_time:
                exists = SwitchConfigBackup.objects.filter(
                    switch=switch, backup_date=backup_date, backup_time=backup_time
                ).exists()
                if exists:
                    continue
            SwitchConfigBackup.objects.create(
                switch=switch,
                config_data=str(r.get('CONFIG_DATA', '') or ''),
                status=str(r.get('STATUS', '') or ''),
                backup_date=backup_date,
                backup_time=backup_time,
            )
        created += 1
    stdout.write(f"  SwitchConfigBackup: {created}건 처리")


# ─────────────────────────────────────────────
# 헬퍼
# ─────────────────────────────────────────────

def _collect_rows(data, table_name):
    """data dict에서 특정 테이블의 모든 row dict 목록 수집"""
    rows = []
    for cols, row_list in data.get(table_name, []):
        for row in row_list:
            if len(row) == len(cols):
                rows.append(dict(zip(cols, row)))
    return rows


def _euckr_fix(text):
    """IPScan latin1→euc-kr 인코딩 오류 복구"""
    if not text:
        return text
    try:
        return text.encode('latin1').decode('euc-kr', errors='replace')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


# ─────────────────────────────────────────────
# Command
# ─────────────────────────────────────────────

MIGRATION_STEPS = [
    ('CPY_INF',        migrate_companies),
    ('DPT_INF',        migrate_departments),
    ('USR_INF/OTH_INF', migrate_persons),
    ('IP_PRN/GRP_INF', migrate_ip_groups),
    ('IP_MNG',         migrate_ip_addresses),
    ('NTWR_DVCS_INF',  migrate_network_devices),
    ('PHN_MNG',        migrate_phones),
    ('RCK_INF',        migrate_racks),
    ('SWT_INF',        migrate_switches),
    ('SWT_PRT_MD_INF', migrate_switch_ports),
    ('ETH_SWT_INF',    migrate_switch_mac_entries),
    ('SWT_CNF_BCK',    migrate_switch_backups),
]


class Command(BaseCommand):
    help = '.sql 백업 파일을 파싱해 신규 DB로 데이터 이전'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sql-file', type=str, default='20260528_sqlbackup.sql',
            help='.sql 백업 파일 경로 (기본: 20260528_sqlbackup.sql)'
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help='실제 저장 없이 파싱/건수만 확인'
        )
        parser.add_argument(
            '--table', type=str, default=None,
            help='특정 원본 테이블만 이전 (예: --table IP_MNG)'
        )

    def handle(self, *args, **options):
        sql_file = options['sql_file']
        dry_run = options['dry_run']
        only_table = options.get('table')

        if not os.path.isabs(sql_file):
            from django.conf import settings
            sql_file = os.path.join(settings.BASE_DIR, sql_file)

        if not os.path.exists(sql_file):
            raise CommandError(f"SQL 파일을 찾을 수 없습니다: {sql_file}")

        mode = '[DRY-RUN]' if dry_run else '[실행]'
        self.stdout.write(self.style.SUCCESS(f"{mode} migrate_legacy 시작"))
        self.stdout.write(f"  파일: {sql_file}")

        self.stdout.write("파싱 중...")
        data = parse_sql_file(sql_file)

        found_tables = sorted(data.keys())
        self.stdout.write(f"  감지된 테이블 {len(found_tables)}개: {', '.join(found_tables)}")

        skipped = [t for t in found_tables if t in SKIP_TABLES]
        if skipped:
            self.stdout.write(self.style.WARNING(f"  제외 테이블: {', '.join(skipped)}"))

        self.stdout.write("이전 시작...")
        try:
            with transaction.atomic():
                for label, func in MIGRATION_STEPS:
                    if only_table and only_table.upper() not in label.upper():
                        continue
                    self.stdout.write(f"▶ {label}")
                    func(data, dry_run, self.stdout)

                if dry_run:
                    raise _DryRunRollback()

        except _DryRunRollback:
            self.stdout.write(self.style.WARNING("DRY-RUN 완료 — DB 변경 없음 (롤백)"))
            return

        self.stdout.write(self.style.SUCCESS("migrate_legacy 완료"))
        self._print_summary()

    def _print_summary(self):
        from assets.models import Company, Department, Person, IpGroup, IpAddress, NetworkDevice, Phone
        from switches.models import Rack, Switch, SwitchPort, SwitchMacEntry, SwitchConfigBackup

        self.stdout.write("\n--- 이전 결과 요약 ---")
        self.stdout.write(f"  Company:           {Company.objects.count():>6}")
        self.stdout.write(f"  Department:        {Department.objects.count():>6}")
        self.stdout.write(f"  Person(employee):  {Person.objects.filter(person_type='employee').count():>6}")
        self.stdout.write(f"  Person(other):     {Person.objects.filter(person_type='other').count():>6}")
        self.stdout.write(f"  IpGroup:           {IpGroup.objects.count():>6}")
        self.stdout.write(f"  IpAddress:         {IpAddress.objects.count():>6}")
        self.stdout.write(f"  NetworkDevice:     {NetworkDevice.objects.count():>6}")
        self.stdout.write(f"  Phone:             {Phone.objects.count():>6}")
        self.stdout.write(f"  Rack:              {Rack.objects.count():>6}")
        self.stdout.write(f"  Switch:            {Switch.objects.count():>6}")
        self.stdout.write(f"  SwitchPort:        {SwitchPort.objects.count():>6}")
        self.stdout.write(f"  SwitchMacEntry:    {SwitchMacEntry.objects.count():>6}")
        self.stdout.write(f"  SwitchConfigBackup:{SwitchConfigBackup.objects.count():>6}")


class _DryRunRollback(Exception):
    pass
