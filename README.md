# GNTEL IT 통합 관리 시스템

사내 IT 자산(IP/전화번호/스위치) 관리, 정기점검, 계정 작업 내역을 통합 관리하는 Django 기반 웹 시스템입니다.

---

## 기술 스택

| 항목 | 내용 |
|------|------|
| Framework | Django 5.x |
| Language | Python 3.11+ |
| Database | MariaDB (로컬/운영 모두) |
| DB Driver | PyMySQL (mysqlclient 호환 모드) |
| Template | Django Template (HTML/CSS 직접 작성) |
| Excel Export | openpyxl |
| 스위치 통신 | netmiko / paramiko (Juniper) |
| GW 동기화 | pyodbc (MS SQL Server) |

---

## 앱 구조

```
config/          # Django 프로젝트 설정
core/            # AuditLog, 공통 management commands
assets/          # IP, 전화번호, 사용자/부서/회사 관리
switches/        # 스위치, 랙, 포트, 설정 백업
inspection/      # 월별 정기점검, 서버 마스터
accounts_work/   # 계정 작업 내역
```

---

## 로컬 개발 환경 설정

### 1. 가상환경 생성 및 패키지 설치

```bash
# uv 사용 (권장)
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt

# 또는 pip 사용
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 DB 접속 정보 입력
```

`.env` 필수 항목:

```
SECRET_KEY=<랜덤 문자열>
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=it_manager
DB_USER=<MariaDB 사용자>
DB_PASSWORD=<MariaDB 비밀번호>
```

### 3. MariaDB 데이터베이스 생성

```sql
CREATE DATABASE it_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 마이그레이션 실행

```bash
python manage.py migrate
```

### 5. 서버 초기 데이터 로드 (정기점검 서버 9종)

```bash
python manage.py loaddata inspection/fixtures/servers.json
```

### 6. 관리자 계정 생성

```bash
python manage.py createsuperuser
```

### 7. 개발 서버 실행

```bash
python manage.py runserver
```

---

## 레거시 데이터 이전

기존 `network_db` 백업 `.sql` 파일로부터 신규 DB로 데이터를 이전합니다.

```bash
# 이전 내용 확인 (DB 변경 없음)
python manage.py migrate_legacy --sql-file 20260528_sqlbackup.sql --dry-run

# 실제 이전 실행
python manage.py migrate_legacy --sql-file 20260528_sqlbackup.sql

# 특정 테이블만 이전
python manage.py migrate_legacy --sql-file 20260528_sqlbackup.sql --table IP_MNG
```

> `.sql` 파일은 용량/보안상 git에 포함하지 않습니다. 프로젝트 루트에 직접 배치하세요.

---

## 외부 데이터 동기화 (사내망 접속 후 사용)

아래 커맨드는 `.env`에 해당 접속 정보가 설정된 경우에만 동작합니다.

| 커맨드 | 설명 | 필요 환경변수 |
|--------|------|--------------|
| `python manage.py sync_gw_users` | 그룹웨어 MS SQL Server → Person/Department 동기화 | `GW_ALL_*` |
| `python manage.py sync_ipscan` | IPScan MariaDB → NetworkDevice 동기화 | `IPSCAN_*` |
| `python manage.py sync_switch_ports` | 스위치 SSH → SwitchPort/SwitchMacEntry 동기화 | `CODING_*`, `SWITCH_*` |
| `python manage.py backup_switch_config` | 스위치 SSH → SwitchConfigBackup 저장 | `CODING_*`, `SWITCH_*` |

> 접속 정보가 없으면 명확한 오류 메시지와 함께 종료됩니다. 모든 커맨드는 `--dry-run` 옵션을 지원합니다.

---

## 주요 URL (구현 예정)

```
/                           대시보드
/accounts/login/            로그인
/assets/ip/                 IP 관리
/assets/phone/              전화번호 관리
/assets/switch/             스위치 관리
/assets/switch/backups/     스위치 백업
/inspection/                정기점검 목록
/inspection/<yyyymm>/export/ Excel Export
/accounts-work/             계정 작업 내역
/logs/                      변경 로그
/admin/                     관리자 페이지
```

---

## 정기점검 Excel Export

기준 양식: `●월간 서버 점검리스트_2026년_4월.xlsx` (프로젝트 루트에 별도 배치)

```bash
# 해당 월 점검 데이터를 양식에 맞춰 Excel 생성
GET /inspection/2026-05/export/
```

> 원본 양식 파일은 git에 포함되지 않습니다. 프로젝트 루트에 직접 배치하세요.

---

## 보안 주의사항

- `.env` 파일은 절대 git에 커밋하지 않습니다.
- `script/json/credentials.json`, `encryption_key.key`는 gitignore에 포함됩니다.
- 스위치 SSH 계정은 반드시 환경변수(`SWITCH_USER`, `SWITCH_PASSWORD`)로 관리합니다.
- 스위치 명령 전송 시 위험 명령(`set`, `delete`, `commit`, `request system`)은 재확인 또는 차단됩니다.

---

## 현재 구현 진행 상황

- [x] Django 프로젝트 및 앱 구조 생성
- [x] MariaDB 연결 설정 (PyMySQL)
- [x] 전체 모델 설계 및 migrations 생성
- [x] Django Admin 등록
- [x] 레거시 데이터 이전 command (`migrate_legacy`)
- [ ] 로그인/로그아웃/대시보드 UI
- [ ] IP 관리 CRUD
- [ ] 전화번호 관리 CRUD
- [ ] 스위치 관리 / 포트 / 백업
- [ ] 정기점검 + Excel Export
- [ ] 계정 작업 관리
- [ ] AuditLog / 변경 로그
- [ ] 스위치 실시간 Status / 명령어 전송
- [ ] GW/IPScan/스위치 데이터 동기화 커맨드
