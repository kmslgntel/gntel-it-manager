# Claude Work Order — 사내 IT 통합 관리 시스템 구현 지시문

아래 내용을 Claude Code에게 그대로 전달하면 됩니다.

---

# 사내 IT 통합 관리 시스템 신규 구축 지시

너는 지금부터 사내 IT 통합 관리 시스템을 신규 구축한다.

작업 시작 전에 반드시 아래 5개 파일을 모두 처음부터 끝까지 읽고 이해해라.

1. `system_requirements.md`
   - 신규 시스템의 최종 기준 문서다.
   - 기술 스택, 새 DB 구조, 앱 구조, URL 설계, 모델 설계, 구현 방향은 이 문서를 최우선으로 따른다.

2. `legacy_system_analysis.md`
   - 기존 IT_MNG 시스템의 기능 설명서다.
   - 기존 시스템의 메뉴, 화면, API, 데이터 흐름, 사용자가 쓰던 업무 기능을 파악하기 위한 문서다.
   - 기존 코드 구조, Raw SQL 방식, URL 이름, JS 구조를 그대로 복사하지 말고, 기능과 업무 흐름만 새 시스템에 재구현한다.

3. `feature_migration_map.md`
   - 기존 기능을 신규 시스템에 어떻게 반영할지 정리한 매핑표다.
   - 기존 기능 누락 여부를 확인하는 체크리스트로 사용한다.

4. `ui_design_guide.md`
   - UI/UX, 색상, 폰트, 레이아웃, anti-pattern 기준 문서다.
   - HTML/CSS는 이 문서를 기준으로 직접 구현한다.

5. `database_erd.md`
   - 신규 DB 모델과 관계를 정리한 ERD 문서다.
   - Django 모델 작성과 migration 설계 시 이 문서를 기준으로 관계를 검증한다.

---

## 가장 중요한 작업 방침

문서 안에 `1일차 이후`, `이후`, `여유 시`, `MVP 이후`, `추후`, `검토`라고 적힌 항목도 이번 작업에서는 모두 구현 대상이다.

그 표현들은 기존 계획상의 우선순위일 뿐이며, 현재 요구사항에서는 구현 제외나 연기를 의미하지 않는다.

즉, 이번 작업의 목표는 단순 MVP가 아니라 다음 전체 범위를 가능한 한 모두 완성하는 것이다.

- `system_requirements.md`에 정의된 신규 시스템 기능 전체
- `legacy_system_analysis.md`에 정리된 기존 시스템의 업무 기능 전체
- `feature_migration_map.md`에 정리된 기존 기능 반영 항목 전체

단, 외부 시스템 접속 정보가 없어 실제 연동이 불가능한 부분은 기능을 삭제하거나 TODO로 방치하지 말고, 설정값만 입력하면 동작할 수 있는 구조까지 구현해라.

예:

- 기존 MariaDB 접속 정보가 없으면 `.env.example`과 설정 구조, migration command 골격, dry-run/mock 검증 구조까지 만든다.
- 스위치 SSH 계정이 없으면 netmiko 실행 함수, command view, whitelist, AuditLog 구조까지 만든다.
- Excel 원본 양식이 없으면 기본 export 형식으로 먼저 구현하고, 템플릿 파일이 들어오면 교체 가능한 구조로 만든다.
- GW/IPScan/스위치 포트 수집 정보가 없으면 management command 인터페이스와 설정 구조를 먼저 만든다.

---

## 문서 우선순위

문서 간 내용이 충돌하면 아래 순서를 따른다.

1. `system_requirements.md`의 확정 결정사항
2. 이 지시문의 “모든 기능을 이번 범위에 포함한다”는 방침
3. `feature_migration_map.md`의 기능 매핑표
4. `legacy_system_analysis.md`의 기존 시스템 동작 설명

예시:

- `system_requirements.md`에서 기존 코드는 폐기한다고 했으면 기존 코드를 재사용하지 않는다.
- `legacy_system_analysis.md`에 기존 URL이 `/it_mng/update_ip/`라고 되어 있어도 신규 시스템에서는 새 URL 구조를 사용한다.
- `feature_migration_map.md`에서 어떤 기능 상태가 `이후`라고 되어 있어도 이번 작업의 구현 대상이다.
- 기존 시스템이 Raw SQL 중심이어도 신규 시스템은 Django ORM과 신규 모델 중심으로 구현한다.

---

## 절대 지켜야 할 원칙

1. 기존 코드는 폐기한다.
2. 기존 코드는 참고만 하고 복사하지 않는다.
3. 기존 DB 데이터는 새 DB로 이전해서 사용한다.
4. 운영 코드는 기존 DB에 직접 의존하지 않는다.
5. 모든 신규 테이블은 Django가 관리하는 `managed = True` 모델로 만든다.
6. Docker는 사용하지 않는다.
7. Django Template 기반으로 구현한다.
8. HTML/CSS는 직접 작성한다.
9. 기존 시스템의 업무 기능은 최대한 누락 없이 재구현한다.
10. 기존 URL/API/JS 구조를 그대로 가져오지 않는다.
11. 모든 데이터 변경은 AuditLog에 기록한다.
12. 로그인 필요한 화면은 `@login_required`를 적용한다.
13. POST 요청은 CSRF를 유지한다.
14. 자격증명은 환경변수로 관리하고 코드에 평문 저장하지 않는다.
15. 스위치 명령어 전송은 보안장치를 반드시 둔다.
16. 구현 후 `python manage.py check`를 실행한다.
17. 가능한 범위에서 migration, 테스트, 주요 화면 동작을 검증한다.

---

## 구현 대상 전체 범위

아래 항목은 모두 구현 대상이다.

### 1. 프로젝트 기반

- Django 프로젝트 생성
- 앱 생성
  - `core`
  - `assets`
  - `switches`
  - `inspection`
  - `accounts_work`
- settings 구성
- `.env.example` 작성
- static/templates 구조 구성
- base layout 작성
- 로그인/로그아웃 설정
- 관리자 페이지 설정

### 2. 신규 DB 모델

`system_requirements.md`의 모델 설계를 기준으로 신규 모델을 작성한다.

필수 모델 범위:

- 회사/부서/사용자/기타 사용자 통합 모델
- IP 그룹
- IP 주소
- 네트워크 장비 정보
- 전화번호/내선
- 렉
- 스위치
- 스위치 포트
- 스위치 MAC Entry
- 스위치 설정 백업
- 정기점검 서버 마스터
- 정기점검 월별 Header
- 정기점검 상세
- 계정 작업 내역
- AuditLog

### 3. 데이터 이전

기존 MariaDB `network_db`의 데이터를 새 DB로 이전하는 Django management command를 작성한다.

필수 조건:

- command 예: `python manage.py migrate_legacy`
- 기존 DB 접속 정보는 `LEGACY_DB_*` 환경변수 사용
- 새 DB는 Django default DB 사용
- 기존 DB는 읽기 전용으로만 접근
- 재실행 가능하도록 멱등성 고려
- 무시 대상 테이블은 이전하지 않음
- 이전 후 건수/샘플 검증 출력

이전 대상:

- `CPY_INF`
- `DPT_INF`
- `USR_INF`
- `OTH_INF`
- `IP_GRP_INF`
- `IP_PRN_INF`
- `GRP_INF`
- `IP_MNG`
- `NTWR_DVCS_INF`
- `PHN_MNG`
- `RCK_INF`
- `SWT_INF`
- `SWT_PRT_MD_INF`
- `PRT_CNC_LCT_INF`
- `ETH_SWT_INF`
- `SWT_CNF_BCK`
- `SWT_BCK_INF`

### 4. 인증/기본 화면

- 로그인
- 로그아웃
- 로그인 후 대시보드
- 기본 헤더/사이드바
- staff 전용 관리자 메뉴
- Django admin 등록

### 5. 공통 UI 기능

각 목록 화면에 가능한 범위로 구현한다.

- 검색
- 상세 필터
- 페이지네이션
- 정렬
- Excel 다운로드
- 선택 체크박스
- 일괄 처리 기반 구조
- 사용자 검색/선택 UI

### 6. IP 관리 전체 기능

기존 시스템의 IP 관리 기능을 신규 구조로 재구현한다.

필수 기능:

- IP 통합 목록
- 무선 IP 필터
- 유선 IP 필터
- IP Phone IP 필터
- Server IP 필터
- HCI IP 필터
- 기타 IP 필터 가능 구조
- IP 상세
- IP 등록
- IP 수정
- IP 삭제 또는 할당 해제
- IP 일괄 수정
- IP 일괄 삭제 또는 할당 해제
- 사용자 검색/선택
- 비고 수정
- IPScan 정보 표시
- MAC 표시
- 회사/부서/사용자 표시
- Excel 다운로드
- AuditLog 기록

주의:

- 기존 시스템의 삭제는 실제 row 삭제가 아니라 `USER_ID`, `NOTE` 등을 비우는 할당 해제 성격이었다.
- 신규 시스템에서도 실제 삭제와 할당 해제를 구분해서 안전하게 설계한다.

### 7. 전화번호/내선 관리 전체 기능

필수 기능:

- 전화번호 목록
- 전화번호 상세
- 전화번호 등록
- 전화번호 수정
- 전화번호 삭제 또는 할당 해제
- 전화번호 일괄 수정
- 전화번호 일괄 삭제 또는 할당 해제
- 사용자 검색/선택
- 목적/비고 수정
- 전화기 IP 선택
- IP 연결/해제 시 IP 관리 데이터와 일관성 유지
- IP/MAC 표시
- 회사/부서/사용자 표시
- Excel 다운로드
- AuditLog 기록

### 8. 스위치 관리 전체 기능

필수 기능:

- 스위치 목록
- 렉별 스위치 표시
- 스위치 상세
- 스위치 포트 정보 목록
- 스위치 포트 필터
- 스위치 포트 검색
- 포트 모드 표시
- 아웃렛/AREA/PORT 번호 표시
- VLAN 표시
- MAC 표시
- 연결된 IP/사용자/부서/회사/전화번호 표시
- 스위치 포트 정보 Excel 다운로드
- 스위치 백업 목록
- 날짜/시간별 백업 조회
- 렉별 백업 조회
- 단일 스위치 config 조회
- 단일 config TXT 다운로드
- 렉 단위 ZIP 다운로드
- 날짜/시간 단위 전체 ZIP 다운로드

### 9. 스위치 실시간 Status/명령어 전송

필수 기능:

- `/assets/switch/<pk>/status/` 또는 이에 준하는 신규 URL
- netmiko 기반 Juniper 접속 함수
- 기본 show 명령 실행
- 명령 결과 화면 출력
- `/assets/switch/<pk>/command/` 또는 이에 준하는 신규 URL
- 명령어 입력 화면
- 우선 `show ...` 명령 허용
- 위험 명령 차단 또는 재확인
- 실행자/스위치/명령/결과를 AuditLog에 기록
- `SWITCH_USER`, `SWITCH_PASSWORD` 환경변수 사용
- 접속 실패 시 사용자에게 오류 표시

주의:

- `set`, `delete`, `commit`, `request system` 등 위험 명령은 단순 실행하지 말고 재확인 또는 차단 로직을 둔다.

### 10. 변경 로그/AuditLog

필수 기능:

- AuditLog 모델
- 데이터 변경 시 로그 기록
- IP 변경 로그
- 전화번호 변경 로그
- 스위치 명령 실행 로그
- 계정 작업 변경 로그
- 로그 목록 화면 또는 admin 조회
- 필터 가능한 구조

### 11. 계정 작업 관리

필수 기능:

- 계정 작업 목록
- 계정 작업 등록
- 계정 작업 수정
- 계정 작업 삭제
- 기간 필터
- 시스템 구분 필터
- 작업 유형 필터
- 작업자 필터
- 대상자 필터
- 정기점검 월별 집계에 사용할 수 있는 구조
- AuditLog 기록

시스템 구분 예:

- 그룹웨어
- ERP
- 파일서버 계정
- 파일서버 폴더
- 방화벽

작업 유형 예:

- 추가
- 삭제
- 퇴사처리
- 권한변경
- 폴더 생성
- 폴더명 변경

### 12. 정기점검 관리

필수 기능:

- 서버 마스터 초기 데이터
- 월별 정기점검 생성
- 정기점검 목록
- 정기점검 상세
- 서버별 점검 항목 입력
- 점검 항목 수정
- 점검 결과 특이사항 입력
- 계정 작업 건수 집계
- IPS/메일/백업/Windows/V3/디스크/CPU/RAM/Event Log 항목 입력
- 정기점검 Excel Export

서버 초기값:

- 그룹웨어
- ERP
- 파일서버
- 방화벽
- 스팸차단
- DNS
- 백업
- 내부통제
- HCI

### 13. Excel Export

필수 기능:

- IP 목록 Excel
- 전화번호 목록 Excel
- 스위치 포트 정보 Excel
- 정기점검 Excel
- 계정작업 내역 Excel 또는 정기점검 Export 내 포함

주의:

- 기존 제출 양식 파일이 없으면 기본 양식으로 구현한다.
- 추후 템플릿 파일을 넣으면 셀 배치를 맞출 수 있도록 구조화한다.

### 14. 외부 데이터 갱신/수집 인터페이스

기존 시스템의 데이터 갱신 버튼 개념을 신규 구조로 재구현한다.

필수 기능:

- IPScan 데이터 갱신 management command 또는 admin action
- GW 데이터 갱신 management command 또는 admin action
- 스위치 포트 데이터 갱신 management command 또는 admin action
- 실행 결과 로그
- 접속 정보 없을 때 명확한 오류 메시지
- 추후 실제 수집 로직 교체 가능한 구조

### 15. 관리자 계정 관리

필수 기능:

- Django admin 기반 사용자 관리
- staff 권한 사용자만 접근
- 필요 시 간단한 사용자 목록/생성/수정 화면
- 비밀번호 재설정 가능 구조

---

## 구현 순서

아래 순서로 진행해라.

1. 5개 MD 파일 전체 읽기
2. 전체 요구사항 요약
3. 구현 대상 기능 목록 재작성
4. 프로젝트 생성 및 앱 생성
5. settings/.env/static/templates 기본 구성
6. 모델 작성
7. migration 생성 및 적용
8. admin 등록
9. legacy migration command 작성
10. 기본 인증/레이아웃 구현
11. IP 관리 구현
12. 전화번호 관리 구현
13. 스위치 포트/백업 구현
14. AuditLog 구현 및 각 변경 기능에 연결
15. 계정 작업 관리 구현
16. 정기점검 구현
17. Excel Export 구현
18. 스위치 Status/명령어 전송 구현
19. 외부 데이터 갱신 command/admin action 구현
20. 전체 URL 연결
21. `python manage.py check` 실행
22. migration 상태 확인
23. 주요 화면 수동 검증
24. README 또는 실행 방법 정리

---

## 구현 중 의사결정 기준

시간이 부족하거나 선택지가 생기면 아래 기준을 따른다.

1. 데이터 구조 안정성 우선
2. 기존 기능 누락 방지 우선
3. 보안 우선
4. 운영 가능한 단순 구현 우선
5. 화려한 UI보다 명확한 HTML/CSS 우선
6. 자동화보다 수동 입력 가능 구조 우선
7. 외부 연동은 실제 접속 정보가 없으면 mock/설정 인터페이스까지 구현

---

## 금지 사항

아래는 하지 마라.

- 기존 코드를 그대로 복사
- 기존 Raw SQL을 무분별하게 그대로 이식
- 기존 DB를 운영 DB처럼 직접 참조
- Docker 사용
- 자격증명 하드코딩
- 위험 스위치 명령 무검증 실행
- 로그인 없이 데이터 변경 가능하게 만들기
- CSRF 비활성화
- `이후 구현`이라는 이유로 기능 전체를 누락
- 외부 정보가 없다는 이유로 구조 자체를 만들지 않기
- TODO만 남기고 화면/URL/model 없이 끝내기

---

## 검증 명령

구현 후 최소한 아래를 실행해라.

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py showmigrations
```

가능하면 아래도 수행해라.

```bash
python manage.py test
python manage.py migrate_legacy --dry-run
```

---

## 먼저 해야 할 응답

작업을 시작하면 먼저 아래 내용을 요약해라.

1. 5개 문서를 모두 읽었는지
2. 신규 시스템의 기준 문서가 무엇인지
3. 기존 시스템 문서는 어떤 용도로 사용할 것인지
4. `MVP/이후/검토` 항목을 이번 작업에서 어떻게 처리할 것인지
5. 구현할 전체 기능 목록
6. 구현 순서

그 다음 바로 구현을 시작해라.

---

## 최종 목표

최종 결과물은 기존 IT_MNG 시스템의 주요 업무 기능을 모두 포함하면서도, 기존 코드 구조를 버리고 새 Django 구조로 재작성된 사내 IT 통합 관리 시스템이다.

기존 시스템에서 사용하던 기능은 누락하지 않고, 신규 요구사항인 정기점검과 계정작업 관리까지 포함해야 한다.

문서상 `1일차 이후`, `이후`, `여유 시`라고 표현된 기능도 이번 범위에서 모두 구현 대상으로 본다.
