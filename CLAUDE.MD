# 사내 IT 통합 관리 시스템 — Claude Code 진입 문서

너는 지금부터 사내 IT 통합 관리 시스템을 신규 Django 프로젝트로 구현한다.

---

# ★ 최우선 확정 사항 (다른 모든 문서보다 우선) ★

아래 항목은 다른 문서(`system_requirements.md`, `claude_work_order.md`,
`database_erd.md`, `feature_migration_map.md` 등)의 내용과 충돌하면
**무조건 이 블록을 따른다.** 다른 문서에 다르게 적혀 있어도 여기를 우선한다.

## 1. 데이터베이스 = MariaDB (PostgreSQL 아님)
- 새 DB는 PostgreSQL이 아니라 **MariaDB**로 한다. (로컬/운영 모두 MariaDB)
- DB 드라이버는 `mysqlclient`를 사용한다. `psycopg2` / PostgreSQL 관련 내용은 모두 무시한다.
- settings의 DB ENGINE은 `django.db.backends.mysql` 로 한다.
- 다른 문서에 "PostgreSQL 권장"이라고 적혀 있어도 따르지 않는다.
- 새 DB 이름 예: `it_manager` (기존 `network_db`와 분리된 새 스키마/DB).
- charset은 `utf8mb4`.

## 2. 데이터 이전 = .sql 백업 파일 파싱 (기존 DB 직접 접속 안 함)
- 기존 MariaDB 운영 서버에 직접 접속하지 않는다.
- 프로젝트 루트의 **`.sql` 백업 파일(`20260528_sqlbackup.sql`)을 파싱**해서 새 DB로 이전한다.
- `LEGACY_DB_*` 환경변수 접속 방식 대신, `.sql` 파일을 읽는 management command로 구현한다.
- 명령 예: `python manage.py migrate_legacy --sql-file 20260528_sqlbackup.sql`
- 이 백업 파일은 CREATE TABLE 없이 `INSERT IGNORE INTO ...` 문 위주이며,
  MariaDB 11.x / DB명 `network_db` / 문자셋 utf8mb4 기준이다.
- 파싱 시 무시 대상 테이블(아래 4번)은 이전하지 않는다.
- 재실행 가능하도록 멱등성 고려 (이전 전 clear 또는 legacy_id 기준 get_or_create).
- 이전 후 건수/샘플 검증 출력.
- `--dry-run` 옵션도 지원한다.

## 3. 정기점검 서버명 = Excel 양식 기준으로 고정
- 서버 마스터(Server) 초기 데이터의 표시명은 반드시 아래 Excel 열 순서(C~K)와 동일하게 한다.
  - C: 그룹웨어
  - D: ERP
  - E: 파일서버
  - F: 방화벽(VPN)
  - G: SPAMOUT
  - H: DNS, Homepage
  - I: 백업서버
  - J: ICARUS
  - K: HCI
- 다른 문서에 "스팸차단 / DNS / 백업 / 내부통제"로 적혀 있어도 위 Excel 명칭(SPAMOUT / DNS, Homepage / 백업서버 / ICARUS)을 우선한다.
- Excel Export 시 이 명칭이 그대로 열에 매칭되어야 한다.

## 4. 데이터 이전 시 무시할 테이블 (절대 이전 안 함)
`IP_MNG_TEST`, `IP_MNG_LOG_TEST`, `PHN_MNG_tmp`, `USR_INF_250103`,
`USR_INF_TMP`, `ip_mng_backup`, `switch_config_backup`,
그리고 Django 내부 테이블(`auth_*`, `django_*`)도 이전하지 않는다.

## 5. Excel Export 셀 매핑 = excel_mapping.md 사용
- 정기점검 Excel Export의 셀 매핑은 **`excel_mapping.md`** 문서를 그대로 따른다.
- 양식을 다시 분석하지 말고 그 매핑 테이블을 사용한다.
- 기준 양식 파일: `●월간 서버 점검리스트_2026년_4월.xlsx` (프로젝트 루트, 원본 수정 금지, 복사본에 기록).

## 6. 환경변수 (.env.example) — MariaDB 기준
```
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 새 DB (MariaDB)
DB_ENGINE=django.db.backends.mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=it_manager
DB_USER=
DB_PASSWORD=

# 스위치 SSH (Juniper)
SWITCH_USER=
SWITCH_PASSWORD=

# (추후) WinRM / 외부 연동 — 없으면 mock/dry-run
ENABLE_WINRM=False
WINRM_USER=
WINRM_PASSWORD=
```
> 기존 DB 직접 접속을 안 하므로 `LEGACY_DB_*` 는 두지 않는다. (.sql 파일 파싱 방식)

---

# 문서 읽기 순서

먼저 위 "최우선 확정 사항"을 숙지한 뒤, 아래 문서들을 처음부터 끝까지 모두 읽어라.

1. `claude_work_order.md` — 전체 구현 지시문 (작업 범위, 금지사항, 구현 순서, 검증 명령)
2. `system_requirements.md` — 신규 시스템 최종 요구사항 (기술스택/DB/모델/URL/원칙)
3. `legacy_system_analysis.md` — 기존 IT_MNG 분석 (기능 파악용 참고, 코드 복사 금지)
4. `feature_migration_map.md` — 기존 기능 → 신규 매핑 체크리스트 (1/2순위/조건부 모두 구현 대상)
5. `ui_design_guide.md` — UI/UX/색상/폰트/레이아웃 기준 (HTML/CSS 직접 구현)
6. `database_erd.md` — 신규 DB 모델/관계 ERD (모델·migration 검증 기준)
7. `excel_mapping.md` — 정기점검 Excel Export 셀 매핑 (5번 항목)

문서 충돌 시 우선순위:
1. **이 문서의 "최우선 확정 사항"**
2. `system_requirements.md`의 확정 결정사항
3. `claude_work_order.md`의 "모든 기능을 이번 범위에 포함" 방침
4. `feature_migration_map.md`의 기능 매핑표
5. `legacy_system_analysis.md`의 기존 동작 설명

---

# 중요한 작업 방침

- 기존 코드는 재사용하지 않는다. 참고만 한다.
- 기존 DB 데이터는 .sql 백업 파싱으로 새 DB(MariaDB)에 이전해서 사용한다.
- 운영 코드는 기존 DB에 직접 의존하지 않는다.
- 모든 신규 테이블은 Django `managed = True` 모델로 관리한다.
- Docker는 사용하지 않는다.
- Django Template 기반으로 구현한다.
- HTML/CSS는 `ui_design_guide.md` 기준으로 직접 작성한다. (사용자가 따로 제공하지 않음)
- GNTEL 로고는 `GNTEL_logo.png`를 사용한다.
- 정기점검 Excel Export는 `●월간 서버 점검리스트_2026년_4월.xlsx` + `excel_mapping.md`를 기준으로 한다.
- 모든 데이터 변경은 AuditLog에 기록한다.
- 로그인 필요한 화면은 `@login_required`를 적용한다.
- POST 요청은 CSRF를 유지한다.
- 스위치 명령어 전송은 show 명령 우선 허용하고, 위험 명령은 차단 또는 재확인하며 AuditLog에 기록한다.
- 문서에 있는 1순위/2순위/조건부 필수 항목은 모두 구현 대상이다.
- 외부 접속 정보가 없어 실제 연동이 불가능한 기능은 삭제하지 말고, 설정값만 넣으면 동작 가능한 구조와 mock/dry-run/명확한 오류 처리를 구현한다.

---

# 작업 순서

1. 위 문서들을 모두 읽고 이해한 내용을 요약해라. (특히 "최우선 확정 사항" 6개 항목을 확인했다고 명시)
2. 구현할 전체 기능 목록을 다시 정리해라.
3. `database_erd.md` 기준으로 Django 모델 설계를 확정해라. (DB는 MariaDB)
4. 신규 Django 프로젝트와 앱을 생성해라. (core, assets, switches, inspection, accounts_work)
5. settings(MariaDB), `.env.example`, static, templates 구조를 구성해라.
6. 모델 작성, migration 생성, admin 등록을 진행해라.
7. **.sql 백업 파싱** 기반 데이터 이전 management command(`migrate_legacy`)를 작성해라.
8. 로그인/로그아웃/대시보드/기본 레이아웃을 구현해라. (GNTEL 로고, Pretendard, 블루/시안 팔레트)
9. IP 관리 기능을 구현해라.
10. 전화번호 관리 기능을 구현해라.
11. 스위치 관리/포트/백업 기능을 구현해라.
12. 정기점검 기능과 Excel Export를 구현해라. (서버명 Excel 기준, excel_mapping.md 셀 매핑)
13. 계정 작업 관리 기능을 구현해라.
14. AuditLog와 변경 로그 조회 기능을 구현해라.
15. 스위치 Status 조회/명령어 전송 기능을 구현해라. (Juniper, netmiko, 화이트리스트)
16. 외부 데이터 갱신 command/admin action 구조를 구현해라. (mock/dry-run)
17. 전체 URL을 연결해라.
18. `python manage.py check`를 실행해라.
19. `python manage.py makemigrations --check --dry-run`을 실행해라.
20. 가능한 경우 `python manage.py test`, `python manage.py migrate_legacy --dry-run`도 실행해라.
21. 실행 방법과 남은 환경변수 설정 항목을 README에 정리해라.

먼저 문서들을 모두 읽은 뒤, 네가 이해한 전체 범위와 구현 순서를 요약하고 바로 구현을 시작해라.
요약에는 반드시 "최우선 확정 사항"의 DB=MariaDB, .sql 파싱 이전, 서버명 Excel 기준을 어떻게 반영할지 포함해라.