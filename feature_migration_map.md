# Feature Migration Map — 기존 IT_MNG 기능 → 신규 시스템 반영

이 문서는 `legacy_system_analysis.md`에 정리된 기존 시스템 기능을 신규 Django 시스템에 빠짐없이 반영하기 위한 체크리스트입니다.

## 문서 역할

- `system_requirements.md`가 신규 시스템의 기준 문서입니다.
- `legacy_system_analysis.md`는 기존 기능 확인용 참고 문서입니다.
- 이 문서는 두 문서 사이의 연결표입니다.
- 기존 코드/URL/JS 구조는 그대로 복사하지 않습니다.
- 기존 사용자가 쓰던 업무 기능과 데이터 의미만 신규 구조로 재구현합니다.

## 구현 우선순위 기준

현재 방침에서는 이 문서의 기능을 모두 이번 구축 범위에 포함한다.

아래 표의 `구현 우선순위`는 제외 여부가 아니라 작업 순서를 의미한다.

- 1순위: 기반 기능으로 먼저 구현
- 2순위: 1순위 다음에 반드시 구현
- 조건부 필수: 외부 접속 정보나 정책 결정이 필요하지만, 가능한 범위까지 인터페이스/mock/dry-run/설정 구조를 구현
- 제외: 신규 시스템에서 명시적으로 제외. 단, 사용자가 다시 지시하면 구현 대상으로 전환

---

## 1. 인증/기본 화면

| 기존 기능 | 기존 근거 | 신규 구현 위치 | 반영 범위 | 구현 우선순위 | 비고 |
|---|---|---|---|---|---|
| 로그인 | `/it_mng/login/`, Django Auth | `/accounts/login/` 또는 Django 기본 auth | 로그인 필수 | 1순위 | Django 기본 Auth 사용 |
| 로그아웃 | `/it_mng/logout/` | `/accounts/logout/` | POST 로그아웃 | 1순위 | CSRF 유지 |
| 메인 화면 | `/it_mng/home/` | `/` 대시보드 | 메뉴 진입 화면 | 1순위 | 기존 업데이트 박스는 선택 |
| staff 전용 계정 관리 | `계정 관리`, `is_staff` | Django admin 우선 | 관리자 계정 CRUD | 1순위 | 전용 화면까지 구현 |

---

## 2. 공통 UI/테이블 기능

| 기존 기능 | 기존 근거 | 신규 구현 위치 | 반영 범위 | 구현 우선순위 | 비고 |
|---|---|---|---|---|---|
| 일반 검색 | 공통 검색 입력 | 각 목록 View/Form | 서버사이드 검색 우선 | 1순위 | JS 대량 렌더링 대신 Django template |
| 하이라이트 검색 | `searchManager.js` | 선택 구현 | 필요 시만 | 2순위 | 2순위로 구현 |
| 상세 필터 | 대역/그룹/항목수 | 목록 페이지 필터 | 그룹/대역 필터 | 1순위 | IP/스위치 우선 |
| 페이지네이션 | 100/200/500/전체 | Django Paginator | 기본 100개 | 1순위 | 전체 보기 선택 가능하면 좋음 |
| 정렬 | 테이블 헤더 클릭 | 서버사이드 order 파라미터 | 주요 컬럼 | 2순위 | 1순위 완료 후 구현 |
| 전체 선택 | 체크박스 | 일괄 수정/삭제 화면 | IP/전화 | 2순위 | CRUD 단계에서 구현 |
| Excel 다운로드 | IP/전화/스위치 | 각 export view | 주요 목록 export | 1순위/2순위 | 정기점검 export는 1순위 |

---

## 3. IP 관리

| 기존 기능 | 기존 근거 | 신규 구현 위치 | 반영 범위 | 구현 우선순위 | 비고 |
|---|---|---|---|---|---|
| IP 통합 조회 | `/it_mng/get_ip_data/` | `/assets/ip/` | 전체 IP 목록 | 1순위 | 기존 데이터 이전 후 조회 |
| 무선 IP | `PARENT_ID=10001` | `/assets/ip/?group=wireless` 또는 필터 | 그룹 필터 | 1순위 | 명칭은 새 그룹 모델 기준 |
| 유선 IP | `PARENT_ID=10000` | `/assets/ip/?group=wired` 또는 필터 | 그룹 필터 | 1순위 |  |
| IP Phone IP | `PARENT_ID=10002` | `/assets/ip/?group=phone` 또는 필터 | 그룹 필터 | 1순위 | 전화번호 IP 후보와 연결 |
| Server IP | `PARENT_ID=10003` | `/assets/ip/?group=server` 또는 필터 | 그룹 필터 | 1순위 |  |
| HCI IP | `PARENT_ID=10004` | `/assets/ip/?group=hci` 또는 필터 | 그룹 필터 | 1순위 |  |
| IP 단건 수정 | `/it_mng/update_ip/` | `/assets/ip/<pk>/edit/` | 사용자/비고 수정 | 2순위 | 2순위로 구현 |
| IP 단건 삭제 | `/it_mng/delete_ip/` | `/assets/ip/<pk>/delete/` | 실제 삭제가 아닌 할당 해제 | 2순위 | 기존 동작 유지 권장 |
| IP 일괄 수정 | `/it_mng/bulk_update_ip/` | `/assets/ip/bulk-edit/` | 다중 사용자/비고 적용 | 2순위 |  |
| IP 일괄 삭제 | `/it_mng/bulk_delete_ip/` | `/assets/ip/bulk-clear/` | 다중 할당 해제 | 2순위 |  |
| 사용자 검색/선택 | `get_user_data`, client filtering | Person 검색 API/폼 | 이름 검색 후 선택 | 2순위 | CRUD 단계에서 필요 |

---

## 4. 전화번호/내선 관리

| 기존 기능 | 기존 근거 | 신규 구현 위치 | 반영 범위 | 구현 우선순위 | 비고 |
|---|---|---|---|---|---|
| 전화번호 목록 조회 | `/it_mng/phone_management/` | `/assets/phone/` | 내선/사용자/IP/MAC 표시 | 1순위 | 데이터 이전 후 조회 |
| 전화번호 단건 수정 | `/it_mng/update_phone/` | `/assets/phone/<pk>/edit/` | 사용자/목적/비고/IP 연결 | 2순위 | 기존처럼 IP_MNG도 동기화 필요 |
| 전화번호 단건 삭제 | `/it_mng/delete_phone/` | `/assets/phone/<pk>/delete/` | 할당 해제 | 2순위 | 실제 row 삭제 아님 |
| 전화번호 일괄 수정 | `/it_mng/bulk_update_phone/` | `/assets/phone/bulk-edit/` | 다중 수정 | 2순위 |  |
| 전화번호 일괄 삭제 | `/it_mng/bulk_delete_phone/` | `/assets/phone/bulk-clear/` | 다중 할당 해제 | 2순위 |  |
| 전화기 IP 선택 모달 | `/it_mng/phone_ip_data/` | 전화 수정 폼 내부 검색 | 사용 가능한 전화기 IP 선택 | 2순위 | CRUD 구현 시 필요 |

---

## 5. 스위치 관리

| 기존 기능 | 기존 근거 | 신규 구현 위치 | 반영 범위 | 구현 우선순위 | 비고 |
|---|---|---|---|---|---|
| 스위치 목록 | `SWT_INF`, `RCK_INF` | `/assets/switch/` | 렉/스위치 목록 | 1순위 |  |
| 스위치 포트 정보 조회 | `/it_mng/switch_port_mode_data/` | `/assets/switch/<pk>/ports/` 또는 `/assets/switch/ports/` | 포트/모드/아웃렛/VLAN/MAC/IP/사용자 | 1순위 | 기존 핵심 조회 기능 |
| 스위치 포트 Excel | `/it_mng/export_switch_port_mode_data/` | `/assets/switch/ports/export/` | xlsx 다운로드 | 2순위 | 2순위로 구현 |
| 스위치 백업 목록 | `/it_mng/switch_backup_data/` | `/assets/switch/backups/` | 백업 날짜/스위치/설정 조회 | 1순위 | 기존 데이터 이전 필요 |
| 전체 백업 ZIP | `/switch_backup_download/datetime/` | `/assets/switch/backups/download/datetime/` | ZIP 다운로드 | 2순위 |  |
| 렉 단위 백업 ZIP | `/switch_backup_download/rack/` | `/assets/switch/backups/download/rack/` | ZIP 다운로드 | 2순위 |  |
| 단일 설정 TXT | `/switch_backup_download/single/` | `/assets/switch/backups/download/single/` | TXT 다운로드 | 2순위 |  |
| 실시간 Status | 신규 요구 | `/assets/switch/<pk>/status/` | netmiko show 명령 | 2순위 | 2순위로 구현 |
| 명령어 전송 | 신규 요구 | `/assets/switch/<pk>/command/` | show 명령 우선, 감사로그 | 2순위 | 안전장치 필수 |

---

## 6. 변경 로그/감사 로그

| 기존 기능 | 기존 근거 | 신규 구현 위치 | 반영 범위 | 구현 우선순위 | 비고 |
|---|---|---|---|---|---|
| 전체 로그 조회 | `/it_mng/log_data/` | `/logs/` 또는 admin | 변경 내역 조회 | 2순위 | 목록 화면 또는 admin 조회 구현 |
| IP LOG | `table_name='IP_MNG'` | AuditLog 필터 | IP 변경 로그 | 2순위 | 신규 테이블명 기준 |
| 전화번호 LOG | `table_name='PHN_MNG'` | AuditLog 필터 | 전화 변경 로그 | 2순위 | 신규 테이블명 기준 |
| 데이터 변경 감사 | `CHANGE_LOG` | `core.AuditLog` | create/update/delete 기록 | 1순위/2순위 | 데이터 변경 기능부터 적용 |

---

## 7. 외부 데이터 갱신/수집

| 기존 기능 | 기존 근거 | 신규 구현 위치 | 반영 범위 | 구현 우선순위 | 비고 |
|---|---|---|---|---|---|
| IPScan 데이터 갱신 | `/it_mng/ipscan_data_update/` | management command 또는 admin action | 수집 스크립트 실행 개념 | 조건부 필수 | 1일차는 기존 데이터 이전 우선 |
| GW 데이터 갱신 | `/it_mng/gw_data_update/` | management command | 사용자/조직 동기화 | 조건부 필수 | GW DB view 정보 필요 |
| 스위치 포트 데이터 갱신 | `/it_mng/switch_port_data_update/` | management command | 스위치 MAC/포트 갱신 | 2순위 | netmiko/기존 수집 방식 검토 |

---

## 8. 신규 기능

| 신규 기능 | 신규 구현 위치 | 반영 범위 | 상태 | 비고 |
|---|---|---|---|---|
| 정기점검 | `/inspection/` | 서버별 월간 점검 입력/저장 | 1순위 | 기존 시스템에는 없던 핵심 신규 기능 |
| 정기점검 Excel Export | `/inspection/<yyyymm>/export/` | 제출 양식 xlsx 생성 | 1순위 | 기존 Excel 양식 필요 |
| 계정 작업 내역 | `/accounts-work/` 또는 admin | 날짜/시스템/작업유형/작업자/대상/내용 | 1순위 | 정기점검 계정 건수 집계에 사용 |

---

## 9. 전체 구현 범위 요약

이번 구축에서는 다음 기능을 모두 구현 대상으로 봅니다. 먼저 구현할 1순위 항목입니다.

1. 새 Django 프로젝트/앱 구조 생성
2. 신규 managed=True 모델 생성
3. 기존 MariaDB 데이터 → 새 DB 이전
4. IP 목록 조회/검색/필터
5. 전화번호 목록 조회/검색/필터
6. 스위치 목록/포트/백업 조회
7. 정기점검 입력/저장
8. 계정 작업 내역 admin 등록 또는 간단 화면
9. 정기점검 Excel Export

다음은 1순위 이후 이어서 구현할 2순위 항목입니다. 구현 제외가 아닙니다.

1. IP/전화번호 전체 CRUD 고도화
2. 일괄 수정/삭제
3. 스위치 명령어 전송
4. 실시간 데이터 수집 자동화
5. 기존 UI의 세부 JS UX 완전 재현
6. 관리자 계정 전용 화면 고도화
