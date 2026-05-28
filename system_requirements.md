# System Requirements — 사내 IT 통합 관리 시스템

Claude Code가 이 프로젝트 작업 시 반드시 참고할 컨텍스트 문서입니다. 작업 시작 전 전체를 읽고, 작업 중에도 관련 섹션을 수시로 참고하세요.

---

## 0. 가장 먼저 읽을 것 — 프로젝트 성격과 결정사항

### 무엇을 하는가

사내 IT 관리 시스템을 **완전히 새로 구축**합니다. 기존에 Django로 만든 시스템이 있으나 스파게티 코드라 **코드는 전부 폐기**하고, **DB 데이터만 재활용(새 DB로 이전)** 합니다.

### 확정된 결정사항

1. **기존 코드 폐기** — 기존 소스는 참고하지 않음. 처음부터 깨끗하게 새로 작성.
2. **데이터는 새 DB로 이전** — 기존 `network_db`(MariaDB)의 자산 데이터(IP/전화/스위치)를 새 시스템의 새 DB로 마이그레이션해서 사용. 기존 DB에 직접 의존하지 않음.
3. **자산(IP/전화/스위치)은 조회 + 수정/추가 모두 새로 구현** — 단순 조회만이 아니라 CRUD 전체.
4. 프레임워크 **Django**, **Docker 미사용**, **HTML/CSS 직접 작성**.

### 개발 조건과 현재 구현 범위 (중요)

- 사내 1인 개발, 기간 **1일** 기준으로 최대한 빠르게 구축한다.
- 현재 방침은 단순 MVP가 아니라 **자산 CRUD 전체 + 정기점검 + 계정작업 + 스위치 명령어 전송까지 모두 이번 구축 범위에 포함**하는 것이다.
- 문서에 남아 있는 `이후`, `여유 시`, `검토`, `MVP 이후` 표현은 일정상 우선순위 표현일 뿐이며 구현 제외를 의미하지 않는다.
- 외부 접속 정보가 없어 실제 연동이 불가능한 기능은 삭제하지 말고, 설정값만 넣으면 동작할 수 있는 구조와 명확한 오류/Mock/Dry-run 경로까지 구현한다.

---

## 0-1. 문서 역할 분리 — Requirements vs Legacy Analysis

이 프로젝트에서 두 문서는 역할이 다릅니다. Claude Code/Hermes가 작업할 때는 아래 기준을 반드시 따른다.

### `system_requirements.md`의 역할 — 신규 시스템 기준 요구사항 문서

이 문서는 **새로 구축할 시스템의 최종 요구사항/결정사항/작업 지시서**이다.

- 신규 시스템의 Source of Truth로 사용한다.
- 기술 스택, 앱 구조, 새 DB 스키마, URL, 작업 우선순위는 이 문서를 따른다.
- 기존 코드 재사용 여부, 데이터 이전 방식, 1일차 범위 등 의사결정은 이 문서가 우선한다.
- 구현자가 실제로 따라야 할 작업 순서와 범위는 이 문서의 10번 작업 순서를 기준으로 한다.

### `legacy_system_analysis.md`의 역할 — 기존 시스템 분석 문서

`legacy_system_analysis.md`는 **기존 시스템에 어떤 기능이 있었는지 확인하기 위한 참고 문서**이다.

- 기존 시스템의 메뉴, 화면, API, 데이터 흐름, UX 동작을 빠짐없이 파악하기 위한 자료로 사용한다.
- 기존 코드를 그대로 따라 구현하라는 뜻이 아니다.
- 기존 Raw SQL, JS 구조, URL 이름, 테이블명을 새 시스템에 그대로 가져오지 않는다.
- 단, 사용자가 기존 시스템에서 사용하던 기능/업무 흐름은 누락되지 않도록 체크리스트로 활용한다.

### 우선순위 규칙

두 문서가 충돌하면 다음 순서를 따른다.

1. `system_requirements.md`의 확정 결정사항
2. `feature_migration_map.md`의 기존 기능 반영 범위
3. `legacy_system_analysis.md`의 기존 동작 설명

예시:

- `legacy_system_analysis.md`에 기존 URL이 `/it_mng/update_ip/`로 되어 있어도 새 시스템은 `/assets/ip/<pk>/edit/` 구조를 우선한다.
- `legacy_system_analysis.md`에 기존 DB 테이블명이 `IP_MNG`로 되어 있어도 새 시스템은 Django 신규 모델 `IpAddress`를 우선한다.
- `legacy_system_analysis.md`의 기존 화면 기능인 검색/페이지네이션/일괄수정/Excel 다운로드는 새 UI 방식으로 재구현한다.

### 기존 기능을 가져오는 기준

기존 시스템에서 가져올 것은 **업무 기능과 데이터 의미**이고, 가져오지 않을 것은 **스파게티 코드 구조와 Raw SQL 중심 구현 방식**이다.

가져온다:

- IP 관리 업무 흐름
- 전화번호/내선 관리 업무 흐름
- 스위치 포트 정보 조회
- 스위치 설정 백업 조회/다운로드
- 변경 로그 조회
- 관리자 계정 관리
- IPScan/GW/스위치 데이터 갱신 개념
- 검색, 필터, 페이지네이션, Excel Export 등 사용자 경험

가져오지 않는다:

- 기존 Django 앱/파일 구조
- 기존 URL/API 이름
- 기존 Raw SQL 중심 View 구현
- 기존 JS에서 HTML을 대량 생성하는 구조
- 기존 DB에 운영 중 직접 의존하는 구조

### 기능 누락 방지 방식

기존 기능은 `feature_migration_map.md`에서 신규 구현 위치와 반영 범위를 추적한다.

- `legacy_system_analysis.md`를 읽고 기존 기능을 목록화한다.
- 각 기능을 새 시스템의 앱/URL/모델에 매핑한다.
- 전체 구현 대상으로 관리하되, 우선순위와 외부 정보 필요 여부를 구분한다.
- 구현 중 기능이 추가로 발견되면 `feature_migration_map.md`에 먼저 반영한 뒤 구현한다.

---

## 1. 기술 스택

| 계층     | 기술                                               |
| ------ | ------------------------------------------------ |
| 프레임워크  | Django 5.x                                       |
| 언어     | Python 3.11+                                     |
| 템플릿    | Django Template (HTML 직접 작성)                     |
| 스타일    | CSS 직접 작성                                        |
| 새 DB   | **PostgreSQL 16 권장** (또는 MariaDB 유지도 가능 — 3번 참고) |
| Excel  | openpyxl                                         |
| 스위치 통신 | netmiko (Juniper, `juniper_junos`)               |
| 데이터 이전 | 일회성 Python 스크립트 (기존 MariaDB → 새 DB)              |

### 개발자 배경

- Django 경험 있음, Python 능숙, HTML/CSS 직접 작성, PowerShell 익숙
- 모든 테이블을 Django가 관리(`managed = True`)하는 깨끗한 구조 선호

---

## 2. 기존 DB에서 추출한 실제 스키마 (이전 원본)

기존 `network_db`(MariaDB) 백업에서 추출. **이 구조의 데이터를 새 스키마로 옮긴다.** 새 스키마 설계의 기준 자료이자, 이전 스크립트의 소스 구조.

### 2.1 IP/네트워크

- **IP_MNG**: `IP_ID`(PK, IP의 32bit 정수 문자열 예 '3232235777'), `IP`('192.168.1.1'), `USER_ID`, `NOTE`, `GROUP_ID`, `START_DATE`, `END_DATE`
- **IP_GRP_INF**: `GROUP_ID`(PK), `GROUP_NAME`(서브넷 '192.168.1.0'), `PARENT_ID`
- **IP_PRN_INF**: `PARENT_ID`(PK), `PARENT_NAME`
- **GRP_INF**: `GROUP_ID`(PK), `GROUP_NAME`, `PARENT_ID` (전화기 IP용 별도 그룹, IN '10016'/'10020')
- **NTWR_DVCS_INF**: `IP_ID`, `IP`, `MAC`, `PROBE_ID`, `HNAME`, `DIVISION`, `USER`, `NOTE` (IPScan 수집 장비정보)
- **IP_MNG_LOG**: `IP_ID`, `IP`, `USER_ID`, `OTHER_ID`, `Note`

### 2.2 사용자/조직

- **USR_INF** (임직원): `USER_ID`(PK 'duzon'), `USER_NAME`, `USER_NAME_EN`, `DEPT_CODE`, `GRADE_NM`(직급), `GRADE_NM_EN`, `USE_YN`(Y/N 재직), `RESIGN_DT`, `EMP_NO`(사번), `EMAIL`, `COCD`, `TEL`, `HP`
- **OTH_INF** (기타 사용자): `OTHER_ID`(PK), `COCD`, `DEPT_CODE`, `OTHER_NAME`, `USE_YN`
- **DPT_INF** (부서): `COCD`, `DEPT_CODE`(PK), `DEPT_NAME`, `DEPT_NAME_EN`, `STEP`, `VIEW_ORDER`, `HIGH_DEPT_CODE`, `USEYN`, `REGDT`
- **CPY_INF** (회사): `COCD`(PK), `CPY_NAME`

### 2.3 전화

- **PHN_MNG**: `PHONE_ID`(PK '1200'), `USER_ID`, `PURPOSE`(용도), `NOTE`, `START_DATE`, `END_DATE`, `IP_ID`

### 2.4 스위치 (Juniper — 인터페이스 'ge-0/0/0.0')

- **RCK_INF**: `RACK_ID`(PK), `RACK_NAME`
- **SWT_INF**: `SWITCH_ID`(PK 정수), `RACK_ID`, `SWITCH_IP`('192.168.4.17'), `SWITCH_SORT`(정렬)
- **SWT_PRT_MD_INF**: `SWITCH_ID`, `INTERFACE`('ge-0/0/0.0'), `PORT_MODE`('trunk'/'access')
- **PRT_CNC_LCT_INF**: `SWITCH_ID`, `INTERFACE`, `AREA_NUMBER`, `PORT_NUMBER`
- **ETH_SWT_INF**: `SWITCH_ID`, `VLAN`, `MAC`, `ENTRY_TYPE`, `AGE`, `INTERFACE` (포트별 학습 MAC)
- **SWT_CNF_BCK**: `SWITCH_ID`, `CONFIG_DATA`(설정텍스트), `STATUS`, `BACKUP_ID`
- **SWT_BCK_INF**: `BACKUP_ID`(PK), `BACKUP_DATE`, `BACKUP_TIME`

### 2.5 공통 로그

- **CHANGE_LOG**: `log_id`(PK), `table_name`, `table_name_kr`, `row_id`, `row_name`, `action_type`, `column_name`, `column_name_kr`, `old_value`, `old_value_kr`, `new_value`, `new_value_kr`, `change_datetime`, `change_date`, `change_time`

### 2.6 무시 (이전 대상 아님 — 테스트/백업 잔재)

`IP_MNG_TEST`, `IP_MNG_LOG_TEST`, `PHN_MNG_tmp`, `USR_INF_250103`, `USR_INF_TMP`, `ip_mng_backup`, `switch_config_backup`

---

## 3. 새 DB 스키마 설계

새 시스템은 **모든 테이블을 Django가 관리**(`managed = True`)합니다. 새 모델은 파이썬/Django 관례(snake_case, 적절한 타입)로 깨끗하게 설계하되, **1일 일정상 기존 구조와 큰 차이 없는 안전한 1:1에 가까운 이전을 기본**으로 합니다. 아래 "개선 포인트"는 여유가 있을 때만 적용.

### 3.1 DB 선택

- **PostgreSQL 16 권장** (새 출발이므로). 기존이 MariaDB라 그대로 MariaDB로 가도 무방.
- Claude Code는 사용자 환경 확인 후 결정. 미정이면 PostgreSQL 가정.

### 3.2 자산 모델 (신규, managed=True)

기존 영문 약어 테이블명 대신 의미 있는 이름 사용. 기존 데이터는 이전 스크립트로 채움.

```python
# assets/models.py

class Company(models.Model):            # ← CPY_INF
    code = models.CharField(max_length=20, unique=True)   # COCD
    name = models.CharField(max_length=100)               # CPY_NAME

class Department(models.Model):         # ← DPT_INF
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    code = models.CharField(max_length=20, unique=True)   # DEPT_CODE
    name = models.CharField(max_length=100)               # DEPT_NAME
    name_en = models.CharField(max_length=100, blank=True)
    high_dept_code = models.CharField(max_length=20, blank=True)
    use_yn = models.CharField(max_length=1, default='Y')

class Person(models.Model):             # ← USR_INF + OTH_INF 통합 (개선 포인트)
    PERSON_TYPE = [('employee','임직원'), ('other','기타')]
    person_type = models.CharField(max_length=10, choices=PERSON_TYPE)
    legacy_id = models.CharField(max_length=50, db_index=True)  # 기존 USER_ID/OTHER_ID 보존
    name = models.CharField(max_length=100)                      # USER_NAME/OTHER_NAME
    name_en = models.CharField(max_length=100, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True)          # GRADE_NM
    emp_no = models.CharField(max_length=50, blank=True)         # EMP_NO
    email = models.EmailField(blank=True)
    tel = models.CharField(max_length=50, blank=True)
    hp = models.CharField(max_length=50, blank=True)
    use_yn = models.CharField(max_length=1, default='Y')         # 재직/사용 여부
    resign_dt = models.CharField(max_length=20, blank=True)
    # 개선: USR/OTH 분기 COALESCE 없이 Person 하나로 조회 가능

class IpGroup(models.Model):            # ← IP_GRP_INF (+ GRP_INF 통합 검토)
    legacy_group_id = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=100)                      # 서브넷 등
    parent_name = models.CharField(max_length=100, blank=True)   # IP_PRN_INF 평탄화
    is_phone_group = models.BooleanField(default=False)          # 기존 GRP_INF 10016/10020 구분

class IpAddress(models.Model):          # ← IP_MNG
    ip = models.GenericIPAddressField()                          # 실제 IP (개선: 정수문자열 대신)
    ip_int = models.BigIntegerField(db_index=True)               # 정렬/정수값 보존 (IP_ID)
    group = models.ForeignKey(IpGroup, on_delete=models.SET_NULL, null=True, blank=True)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)

class NetworkDevice(models.Model):      # ← NTWR_DVCS_INF (IPScan 결과)
    ip_address = models.ForeignKey(IpAddress, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.CharField(max_length=45, blank=True)
    mac = models.CharField(max_length=20, blank=True, db_index=True)
    hostname = models.CharField(max_length=100, blank=True)      # HNAME
    division = models.CharField(max_length=100, blank=True)
    scan_user = models.CharField(max_length=100, blank=True)     # USER
    note = models.TextField(blank=True)

class Phone(models.Model):              # ← PHN_MNG
    phone_id = models.CharField(max_length=20, unique=True)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.ForeignKey(IpAddress, on_delete=models.SET_NULL, null=True, blank=True)
    purpose = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)
```

### 3.3 스위치 모델 (신규, managed=True)

```python
# switches/models.py

class Rack(models.Model):               # ← RCK_INF
    name = models.CharField(max_length=100)

class Switch(models.Model):             # ← SWT_INF
    rack = models.ForeignKey(Rack, on_delete=models.SET_NULL, null=True)
    ip = models.GenericIPAddressField()                          # SWITCH_IP
    sort_order = models.IntegerField(default=0)                  # SWITCH_SORT
    vendor = models.CharField(max_length=30, default='juniper')  # netmiko device_type 결정용
    note = models.TextField(blank=True)

class SwitchPort(models.Model):         # ← SWT_PRT_MD_INF + PRT_CNC_LCT_INF 통합
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, related_name='ports')
    interface = models.CharField(max_length=50)                  # 'ge-0/0/0.0'
    port_mode = models.CharField(max_length=20, blank=True)      # trunk/access
    area_number = models.CharField(max_length=20, blank=True)
    port_number = models.CharField(max_length=20, blank=True)

class SwitchMacEntry(models.Model):     # ← ETH_SWT_INF
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, related_name='mac_entries')
    interface = models.CharField(max_length=50)
    vlan = models.CharField(max_length=20, blank=True)
    mac = models.CharField(max_length=20, db_index=True)
    entry_type = models.CharField(max_length=20, blank=True)
    age = models.CharField(max_length=20, blank=True)

class SwitchConfigBackup(models.Model): # ← SWT_CNF_BCK + SWT_BCK_INF 통합
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, related_name='backups')
    config_data = models.TextField(blank=True)
    status = models.CharField(max_length=20, blank=True)
    backup_date = models.CharField(max_length=20, blank=True)
    backup_time = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 3.4 정기점검 모델 (신규)

```python
# inspection/models.py

class Server(models.Model):             # 점검 대상 9종
    COLLECT_CHOICES = [('manual','수동'),('db-view','DB View'),
                       ('winrm','WinRM'),('ssh','SSH'),('api','API')]
    name = models.CharField(max_length=50, unique=True)
    hostname = models.CharField(max_length=100, blank=True)
    registered_ip = models.CharField(max_length=45, blank=True)
    os = models.CharField(max_length=50)
    collect_method = models.CharField(max_length=20, choices=COLLECT_CHOICES, default='manual')
    is_active = models.BooleanField(default=True)

class Inspection(models.Model):
    inspect_ym = models.CharField(max_length=7, unique=True)     # '2026-05'
    created_by = models.CharField(max_length=50)
    remarks = models.TextField(blank=True)                       # 점검 결과 특이사항
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InspectionDetail(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='details')
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    ip_status = models.CharField(max_length=20, blank=True)      # OK/MISMATCH/N/A
    ip_detected = models.CharField(max_length=45, blank=True)
    event_log_summary = models.TextField(blank=True)
    event_critical = models.IntegerField(null=True, blank=True)
    event_error = models.IntegerField(null=True, blank=True)
    event_warning = models.IntegerField(null=True, blank=True)
    cpu_total_ghz = models.FloatField(null=True, blank=True)
    cpu_usage_pct = models.FloatField(null=True, blank=True)
    ram_total_gb = models.FloatField(null=True, blank=True)
    ram_used_gb = models.FloatField(null=True, blank=True)
    disk_info_json = models.TextField(blank=True)
    disk_health = models.CharField(max_length=20, blank=True)
    last_backup_date = models.DateField(null=True, blank=True)
    win_update_status = models.CharField(max_length=20, blank=True)
    v3_version = models.CharField(max_length=30, blank=True)
    account_create_cnt = models.IntegerField(null=True, blank=True)
    account_change_cnt = models.IntegerField(null=True, blank=True)
    account_delete_cnt = models.IntegerField(null=True, blank=True)
    ips_block_cnt = models.IntegerField(null=True, blank=True)
    mail_normal_cnt = models.IntegerField(null=True, blank=True)
    mail_spam_cnt = models.IntegerField(null=True, blank=True)
    mail_virus_cnt = models.IntegerField(null=True, blank=True)
    mail_ransom_cnt = models.IntegerField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    is_auto_collected = models.BooleanField(default=False)
    class Meta:
        unique_together = ('inspection', 'server')
```

### 3.5 계정 작업 + 감사 로그 (신규)

```python
# accounts_work/models.py
class AccountWork(models.Model):
    SYSTEM_CHOICES = [('groupware','그룹웨어'),('erp','ERP'),
        ('fileserver-account','파일서버 계정'),('fileserver-folder','파일서버 폴더'),('firewall','방화벽')]
    WORK_CHOICES = [('add','추가'),('delete','삭제'),('leave','퇴사처리'),
        ('permission','권한변경'),('folder-create','폴더 생성'),('folder-rename','폴더명 변경')]
    work_date = models.DateField()
    system_type = models.CharField(max_length=30, choices=SYSTEM_CHOICES)
    work_type = models.CharField(max_length=30, choices=WORK_CHOICES)
    operator = models.CharField(max_length=50)
    target = models.CharField(max_length=50)
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# core/models.py
class AuditLog(models.Model):           # ← CHANGE_LOG 역할, 깔끔하게 재설계
    actor = models.CharField(max_length=50)
    action = models.CharField(max_length=50)        # create/update/delete/switch-command
    target_type = models.CharField(max_length=50)
    target_id = models.CharField(max_length=50)
    detail = models.TextField(blank=True)
    acted_at = models.DateTimeField(auto_now_add=True)
```

### 3.6 새 스키마 개선 포인트

- USR_INF + OTH_INF → `Person` 통합 (COALESCE 제거)
- IP_GRP_INF + GRP_INF → `IpGroup` 통합 (`is_phone_group` 플래그)
- IP를 32bit 정수 문자열 대신 `GenericIPAddressField` + 정렬용 `ip_int`
- 스위치 포트 모드/위치 → `SwitchPort` 하나로 통합
- **단, 1일 일정이면 통합을 무리하게 하지 말고, 어렵다면 기존 구조 그대로 1:1 모델링 후 진행**

---

## 4. 데이터 이전 (마이그레이션) 전략

### 방법

일회성 Python 스크립트로 **기존 MariaDB → 새 DB** 이전. Django 관리 명령으로 작성 권장.

```
inspection/management/commands/migrate_legacy.py
→ python manage.py migrate_legacy
```

### 순서 (FK 의존성 고려)

1. Company (CPY_INF)
2. Department (DPT_INF) — Company 참조
3. Person (USR_INF → employee, OTH_INF → other) — Dept/Company 참조
4. IpGroup (IP_GRP_INF + IP_PRN_INF 평탄화, GRP_INF 병합)
5. IpAddress (IP_MNG) — IpGroup/Person 참조, `ip_int = int(IP_ID)`, `ip = IP`
6. NetworkDevice (NTWR_DVCS_INF) — IpAddress 매칭(IP_ID 또는 MAC)
7. Phone (PHN_MNG) — Person/IpAddress 참조
8. Rack (RCK_INF) → Switch (SWT_INF) → SwitchPort (SWT_PRT_MD_INF + PRT_CNC_LCT_INF) → SwitchMacEntry (ETH_SWT_INF) → SwitchConfigBackup (SWT_CNF_BCK + SWT_BCK_INF)

### 이전 시 접속

- 기존 MariaDB는 읽기 전용으로만 접속 (`pymysql` 또는 Django의 두 번째 DB 연결 임시 사용)
- 이전 스크립트에서만 기존 DB 사용, 운영 코드는 새 DB만 바라봄
- 환경변수: `LEGACY_DB_*` (이전용), `DB_*` (새 DB)

### 매핑 주의점

- 이름: `USER_NAME` 있으면 employee, 없고 `OTHER_NAME` 있으면 other → Person.person_type 구분
- 부서/회사: 기존 COALESCE(UI, OI) 로직을 이전 시 Person에 직접 채워 단순화
- IP_ID(정수문자열) → `ip_int`(BigInteger), 실제 IP 문자열 → `ip`
- 날짜 필드들이 빈 문자열('')로 저장돼 있을 수 있음 → 빈 값/None 처리
- 무시 테이블(2.6) 절대 이전하지 말 것

### 멱등성

- 재실행 가능하도록 작성 (이전 데이터 clear 후 재삽입, 또는 legacy_id 기준 get_or_create)

---

## 5. URL 설계

```
/                                       # 대시보드

# 자산: IP
/assets/ip/                             # 목록 + 검색/필터
/assets/ip/new/                         # 등록
/assets/ip/<int:pk>/                    # 상세
/assets/ip/<int:pk>/edit/               # 수정
/assets/ip/<int:pk>/delete/             # 삭제(POST)

# 자산: 전화
/assets/phone/  /new/  /<pk>/  /<pk>/edit/  /<pk>/delete/

# 자산: 스위치
/assets/switch/                         # 목록 (랙/정렬순)
/assets/switch/<int:pk>/                # 상세 (포트/MAC/백업)
/assets/switch/<int:pk>/edit/
/assets/switch/<int:pk>/ports/          # 포트 현황 (기존 스위치 포트모드 쿼리 대체)
/assets/switch/<int:pk>/status/         # 실시간 Status (netmiko)
/assets/switch/<int:pk>/command/        # 명령어 전송(POST)
/assets/switch/backups/                 # config 백업 목록

# 정기점검
/inspection/  /new/  /<str:yyyymm>/  /<str:yyyymm>/export/

# 계정 작업
/accounts-work/  /new/  /<int:pk>/edit/  /<int:pk>/delete/

# 기본
/admin/  /accounts/login/  /accounts/logout/
```

---

## 6. 스위치 Status / 명령어 전송 (Juniper)

- 벤더 Juniper → netmiko `device_type='juniper_junos'`, 접속 IP = `Switch.ip`
- **Status** (`/status/`): `show interfaces terse`, `show chassis routing-engine`, `show system uptime`, `show ethernet-switching table` 등 조회 후 출력. 새 DB의 SwitchPort/MacEntry와 비교 표시 가능
- **명령어 전송** (`/command/`) 안전장치 필수:
    - 화이트리스트: 우선 `show ...` 만 허용
    - 변경 명령(`set`/`delete`/`commit`/`request system`)은 경고 + 재확인 모달
    - 모든 실행 AuditLog 기록 (누가/언제/스위치/명령/결과)
    - `@login_required`, CSRF
- 계정은 환경변수 `SWITCH_USER`/`SWITCH_PASSWORD`

```python
from netmiko import ConnectHandler
def run_switch_command(switch_ip, command):
    # TODO: 화이트리스트 검증, 위험명령 차단, AuditLog 기록
    conn = ConnectHandler(device_type='juniper_junos', host=switch_ip,
        username=os.environ['SWITCH_USER'], password=os.environ['SWITCH_PASSWORD'])
    out = conn.send_command(command)
    conn.disconnect()
    return out
```

---

## 7. 정기점검 항목 (Excel 양식과 동일)

서버별 입력: IP(OK/MISMATCH), 시스템(Event Log 특이사항/건수), H/W(CPU GHz·%, RAM 전체·사용, HDD 디스크별, Disk상태, 최종백업일, Windows·V3 업데이트), 계정(생성/변경/삭제 건수 — AccountWork 집계), IPS(차단건수), 수신메일(정상/스팸·바이러스·랜섬/합계), 점검결과(자유텍스트).

1일 일정: **전 항목 수동 입력 폼 우선.** 자동 수집은 인터페이스만, mock.

점검 결과 예시:

```
- 그룹웨어 등록 1건 (Consulting팀)
- 스팸 차단 필터 4건 업데이트 (견적 사칭메일 외 2건)
- Windows 보안 업데이트 완료(5/10)
```

서버 마스터 초기값: 그룹웨어(db-view), ERP, 파일서버(Synology DSM, ssh), 방화벽(TrusGuard), 스팸차단(SPAMOUT), DNS, 백업, 내부통제, HCI.

---

## 8. 계정 작업 세부 내역

- 필드: 날짜/시스템구분/작업유형/작업자/대상자/세부내용 (모델 3.5)
- 시스템별 작업유형: 그룹웨어·ERP·파일서버계정·방화벽 = 추가/삭제/퇴사처리/권한변경 / 파일서버폴더 = 추가/폴더생성/폴더명변경
- 세부내용 예: `그룹웨어 계정 생성(Consulting "사번")`
- 목록 필터(기간/시스템/작업유형/작업자/대상자) + 페이지네이션
- 시간 부족 시 admin으로 우선 대체

---

## 9. Excel Export (openpyxl)

- `/inspection/<yyyymm>/export/` → .xlsx 다운로드
- 시트1 "정기점검"(서버9종×항목, 기존 양식 배치), 시트2 "계정작업내역"(해당월)
- **[사용자 제공 권장]** 기존 Excel 제출 양식 파일이 있으면 셀 배치 그대로 맞춤

---

## 10. 작업 순서 (1일, 단계적)

### 사전

- 새 DB 종류 결정 (PostgreSQL 권장 / MariaDB 유지 가능)
- 기존 MariaDB 읽기 접속 정보 확보 (이전용)

### 1단계 — 기반 + 데이터 이전 (최우선)

1. `django-admin startproject config .` + 앱 생성: core, assets, switches, inspection, accounts_work
2. settings.py: 새 DB 연결, 앱 등록, static
3. 모든 신규 모델 작성(3번) + makemigrations + migrate
4. **데이터 이전 스크립트**(`migrate_legacy`) 작성 + 실행 → 기존 자산데이터 새 DB로
5. 이전 결과 검증 (건수/샘플 확인)

### 2단계 — 자산 조회 페이지

6. IP 목록(검색/필터) — 이전된 데이터 표시
7. 전화 목록
8. 스위치 목록 + 포트 현황 + config 백업 목록
9. base.html 골격 (HTML/CSS는 개발자가 채움)

### 3단계 — 정기점검 + 계정작업 (핵심 신규)

10. 서버 마스터 초기 데이터
11. 점검 목록 + 상세 입력 폼 + 저장 + 특이사항
12. 계정 작업: admin 등록 + 전용 페이지
13. Excel Export

### 4단계 — 고급 기능/연동까지 구현

14. 자산 수정/추가/삭제/할당해제 폼 (IP/전화/스위치 CRUD)
15. 스위치 Status 조회(netmiko) + 명령어 전송(화이트리스트/재확인/로그)

### 마감

16. 사내 서버 배포 (runserver / gunicorn+nginx), README

> 현재 방침에서는 1~4단계를 모두 이번 구현 범위로 본다. 다만 외부 접속 정보가 필요한 항목은 설정 구조, Mock/Dry-run, 명확한 오류 처리까지 구현한다.

---

## 11. 코딩 규칙

### Django

- 모든 신규 테이블 `managed = True` (Django가 전부 관리)
- 앱 단위 분리(core/assets/switches/inspection/accounts_work)
- 뷰는 함수형(FBV) 우선, 빠르게
- 폼은 Django ModelForm 활용 (자산 CRUD에 유용)
- 모든 데이터 변경은 AuditLog 기록
- 데이터 이전은 management command로, 멱등성 보장

### HTML/CSS

- 사용자가 별도 HTML/CSS를 제공한다고 가정하지 않는다.
- Claude Code가 `ui_design_guide.md` 기준으로 직접 깔끔한 사내 관리자형 UI를 구현한다.
- Pretendard 폰트, GNTEL 로고 기반 Blue/Cyan 팔레트, Header/Sidebar/Main 레이아웃을 사용한다.
- Gradient, 임의 색상, 과한 애니메이션, UI 이모지를 금지한다.
- Django Template 기반으로 구현하고, 복잡한 프론트엔드 프레임워크는 사용하지 않는다.

### 보안

- 스위치 명령 화이트리스트 + 위험명령 재확인 + 로그
- 자격증명(새DB/기존DB/스위치)은 환경변수, 평문 저장 금지
- `@login_required` 전체, POST는 CSRF

### 환경변수 (.env.example)

```
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 새 DB (PostgreSQL 예시)
DB_ENGINE=django.db.backends.postgresql
DB_HOST=
DB_PORT=5432
DB_NAME=it_manager
DB_USER=
DB_PASSWORD=

# 기존 DB (데이터 이전용, 이전 후 불필요)
LEGACY_DB_HOST=
LEGACY_DB_PORT=3306
LEGACY_DB_NAME=network_db
LEGACY_DB_USER=
LEGACY_DB_PASSWORD=

# 스위치 SSH
SWITCH_USER=
SWITCH_PASSWORD=

# (추후) WinRM
ENABLE_WINRM=False
WINRM_USER=
WINRM_PASSWORD=
```

### requirements.txt

```
Django>=5.0
psycopg2-binary        # PostgreSQL (또는 mysqlclient)
pymysql                # 기존 MariaDB 이전 접속용
openpyxl
netmiko
python-dotenv
gunicorn               # 배포(선택)
```

---

## 12. 이번 범위에서 직접 자동 실행하지 않는 항목

- WinRM 자동 수집: 실제 계정/접속 정보가 없으면 인터페이스와 mock/dry-run까지 구현
- TrusGuard / SPAMOUT / Synology 자동 수집: 실제 API/접속 정보가 없으면 설정 구조와 오류 처리까지 구현
- AD SSO + MFA: 이번 버전은 Django 기본 auth로 구현하고, 확장 지점만 남김
- 이중 승인 워크플로우: 기본 AuditLog와 권한 구조를 먼저 구현
- 파일서버 권한변경 / AD 계정생성 실제 실행: 실제 실행 대신 계정 작업 기록/감사 로그 중심으로 구현
- Docker: 사용하지 않음
- 모바일 반응형: PC 업무 화면 우선, 작은 화면에서는 테이블 가로 스크롤 허용

---

## 13. 사용자에게 받아야 할 것

1. **기존 MariaDB 접속 정보** (데이터 이전용 — host/port/db/user/password)
2. **새 DB 종류 결정** (PostgreSQL 권장 / MariaDB 유지)
3. **기존 Excel 제출 양식** (Export 셀 배치 정확히)
4. **스위치 SSH 계정**
5. **기존 페이지 추가 요구사항** (사용자가 별도 작성 예정 — 자산 페이지 화면 구성 등)
6. 그룹웨어 DB view 정보

---

문서 끝. 작업 전 0번(결정사항), 3번(새 스키마), 4번(데이터 이전), 10번(작업 순서)을 반드시 확인하세요. **기존 코드는 참고하지 않습니다. DB 데이터만 4번 전략으로 새 DB에 이전해 재활용합니다.**