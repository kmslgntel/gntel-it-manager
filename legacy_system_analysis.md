# Legacy System Analysis — IT MANAGEMENT SYSTEM

## 1. 문서 목적

이 문서는 현재 `IT_MNG_SITE` 프로젝트의 웹 페이지와 API, 화면 기능, 데이터 흐름을 새 UI/구조 설계에 참고할 수 있도록 정리한 기능 설명서이다.

- 원칙: 기존 코드는 수정하지 않고 읽기/분석만 수행했다.
- 작성 기준: Django URL, View, Template, Static JS/CSS, 모델, 화면 메뉴 구조를 기준으로 기능을 정리했다.
- 결과 파일: `it_mng_result.md`

---

## 2. 프로젝트 개요

### 2.1 서비스 성격

`IT MANAGEMENT SYSTEM`은 사내 IT 자산/네트워크 관리용 웹 시스템이다.
주요 관리 대상은 다음과 같다.

- IP 관리
- 전화번호/내선 관리
- 스위치 포트 정보 관리
- 스위치 설정 백업 조회/다운로드
- 변경 로그 조회
- 관리자 계정 관리
- 외부 데이터 수집 스크립트 실행

### 2.2 기술 스택

- Backend: Django 5.x 기반 Python 웹 애플리케이션
- Database: MySQL/MariaDB 계열 DB 사용
- Frontend: Django Template + Vanilla JavaScript + CSS
- Excel Export: pandas, openpyxl
- 파일 다운로드: HttpResponse, zipfile, BytesIO
- 인증: Django 기본 Auth 사용

### 2.3 프로젝트 규모 참고

분석 시점 기준 주요 파일 수는 다음과 같다.

- Git 추적 파일 수: 94개
- 주요 실제 파일 수: 85개
- 확장자별 대략 구성:
  - Python: 23개
  - HTML: 21개
  - CSS: 18개
  - JavaScript: 11개
  - JSON: 3개
  - Markdown: 2개

---

## 3. 전체 URL 구조

### 3.1 루트 URL

파일: `IT_MNG_SITE/urls.py`

- `/`
  - `/it_mng/login`으로 리다이렉트
- `/it_mng/`
  - `it_mng.urls` 하위 URL 포함

### 3.2 앱 URL 목록

파일: `it_mng/urls.py`

| URL | View | 용도 |
|---|---|---|
| `/it_mng/login/` | `login_view` | 로그인 화면/로그인 처리 |
| `/it_mng/home/` | `home_view` | 로그인 후 메인 화면 |
| `/it_mng/logout/` | `logout_view` | 로그아웃 |
| `/it_mng/get_ip_data/` | `get_ip_data` | IP 통합 조회 데이터 |
| `/it_mng/get-ip-management_data/` | `get_ip_management_data` | IpMngVw 기반 페이지네이션 조회 |
| `/it_mng/search_users/` | `search_users` | 사용자명 검색 API |
| `/it_mng/get_user_data/` | `get_user_data` | 사용자/기타 사용자 통합 목록 조회 |
| `/it_mng/update_ip/` | `update_ip` | IP 단건 사용자/비고 수정 |
| `/it_mng/delete_ip/` | `delete_ip` | IP 단건 등록 정보 삭제 처리 |
| `/it_mng/bulk_update_ip/` | `bulk_update_ip` | IP 일괄 수정 |
| `/it_mng/bulk_delete_ip/` | `bulk_delete_ip` | IP 일괄 삭제 |
| `/it_mng/phone_management/` | `phone_management` | 전화번호 관리 데이터 조회 |
| `/it_mng/phone_ip_data/` | `phone_ip_data` | 전화번호 연결용 IP 후보 조회 |
| `/it_mng/update_phone/` | `update_phone` | 전화번호 단건 수정 |
| `/it_mng/delete_phone/` | `delete_phone` | 전화번호 단건 등록 정보 삭제 |
| `/it_mng/bulk_update_phone/` | `bulk_update_phone` | 전화번호 일괄 수정 |
| `/it_mng/bulk_delete_phone/` | `bulk_delete_phone` | 전화번호 일괄 삭제 |
| `/it_mng/export_ip_data/` | `export_ip_data` | IP/전화번호 목록 Excel 다운로드 |
| `/it_mng/log_data/` | `log_data` | 변경 로그 조회 |
| `/it_mng/switch_port_mode_data/` | `switch_port_mode_data` | 스위치 포트 정보 조회 |
| `/it_mng/export_switch_port_mode_data/` | `export_switch_port_mode_data` | 스위치 포트 정보 Excel 다운로드 |
| `/it_mng/switch_backup_data/` | `switch_backup_data` | 스위치 백업 목록/설정 데이터 조회 |
| `/it_mng/switch_backup_download/datetime/` | `switch_backup_download_datetime` | 특정 백업 날짜/시간 전체 ZIP 다운로드 |
| `/it_mng/switch_backup_download/rack/` | `switch_backup_download_rack` | 특정 렉 단위 ZIP 다운로드 |
| `/it_mng/switch_backup_download/single/` | `switch_backup_download_single` | 특정 스위치 설정 TXT 다운로드 |
| `/it_mng/ipscan_data_update/` | `ipscan_data_update` | IPScan 데이터 수집 스크립트 실행 |
| `/it_mng/gw_data_update/` | `gw_data_update` | 그룹웨어 데이터 수집 스크립트 실행 |
| `/it_mng/switch_port_data_update/` | `switch_port_data_update` | 스위치 포트 데이터 수집 스크립트 실행 |
| `/it_mng/user_list_api/` | `user_list_api` | Django 계정 목록 조회, staff 전용 |
| `/it_mng/users/update/` | `user_update_api` | Django 계정 수정, staff 전용 |
| `/it_mng/users/create/` | `user_create_api` | Django 계정 생성, staff 전용 |

---

## 4. 인증 및 접근 흐름

### 4.1 로그인

화면 파일: `it_mng/templates/login.html`

로그인 화면은 좌우 2단 구조이다.

- 왼쪽: 로고와 `IT MANAGEMENT SYSTEM` 문구
- 오른쪽: 로그인 폼
  - Username 입력
  - Password 입력
  - Sign In 버튼
  - 로그인 실패 시 오류 메시지 출력

Backend 동작:

- `login_view`에서 Django `AuthenticationForm`을 사용한다.
- POST 요청 시 사용자 인증 후 성공하면 `home`으로 리다이렉트한다.
- 실패하면 `Invalid username or password` 메시지를 전달한다.

### 4.2 메인 화면 접근

- `home_view`는 `@login_required`가 적용되어 있다.
- 로그인한 사용자만 `/it_mng/home/`에 접근 가능하다.
- 상단 헤더에 현재 로그인 사용자명이 `{{ request.user.username }} 님` 형식으로 표시된다.

### 4.3 로그아웃

- 메인 화면 우측 상단 로그아웃 버튼을 누르면 POST 방식으로 `logout` URL을 호출한다.
- 로그아웃 후 로그인 페이지로 이동한다.

### 4.4 관리자 권한 화면

- 메인 사이드바의 `계정 관리` 메뉴는 `request.user.is_staff`가 참일 때만 표시된다.
- 계정 관련 API는 `@staff_member_required`가 적용되어 staff 권한 사용자만 접근 가능하다.

---

## 5. 메인 화면 레이아웃

화면 파일: `it_mng/templates/home.html`

### 5.1 전체 구성

메인 화면은 다음 구조로 구성된다.

1. Header
2. Sidebar
3. Main Content
4. 공통 Modal 영역
5. Loading overlay
6. JavaScript 로딩

### 5.2 Header 기능

헤더 좌측:

- GNTEL 로고
- 로고 클릭 시 `/it_mng/home` 이동

헤더 우측:

- `IP 데이터 업데이트` 버튼
- `GW 데이터 업데이트` 버튼
- `스위치 포트 데이터 업데이트` 버튼
- 로그인 사용자명 표시
- 로그아웃 버튼
- 테마 선택 버튼이 JS로 동적 삽입됨

### 5.3 Sidebar 메뉴

사이드바 메뉴 구조:

- IP
  - 무선
  - 유선
  - IP Phone
  - Server
  - HCI
  - 기타는 코드상 존재하지만 주석 처리되어 화면에 표시되지 않음
- 전화번호
- 스위치
  - 스위치 백업
  - 스위치 포트 정보
- LOG
  - IP LOG
  - 전화번호 LOG
- 계정 관리
  - staff 사용자에게만 표시

### 5.4 Main Content 기본 화면

처음 홈 화면에는 업데이트 내역 박스가 표시된다.

포함 내용:

- 20260220 업데이트
  - 계정 관리 탭 추가
  - 계정 생성 및 권한 부여 기능 추가
  - 패스워드 분실 시 사용자 정보 수정으로 재설정 가능
- 20260206 업데이트
  - 긴 값 툴팁 표시
  - 수정 후 새로고침 없이 즉시 반영
  - 팝업창 드래그 이동
  - GW/IP/스위치 포트 모드 자동 조회 기능
  - 스위치 포트 정보 조회 시 10초 이상 소요 가능

---

## 6. Frontend JavaScript 구조

메인 화면은 여러 JS 파일로 기능이 분리되어 있다.

| 파일 | 역할 |
|---|---|
| `static/js/home.js` | 메뉴 라우팅, 헤더 데이터 업데이트 버튼 처리, 로딩 오버레이 |
| `static/js/dataHandler.js` | Backend API 호출 함수 모음 |
| `static/js/initializer.js` | 화면별 HTML 생성, 초기화, 이벤트 연결, Excel/다운로드 처리 |
| `static/js/searchManager.js` | 일반 검색, 하이라이트 검색 |
| `static/js/tableManager.js` | 테이블 렌더링, 행 템플릿, 페이지네이션, 정렬 |
| `static/js/popupHandler.js` | IP/전화번호/계정 팝업, 수정/삭제/일괄처리, 사용자 검색, IP 선택 모달 |
| `static/js/themeHandler.js` | 테마 선택, localStorage 저장/복원 |

### 6.1 화면 전환 방식

`home.js`의 `loadContent(contentType)`이 사이드바 버튼의 진입점이다.

메뉴별 매핑:

| contentType | 실행 함수 | 화면 |
|---|---|---|
| `ip_management` | `load_ip_management` | IP 통합 관리 |
| `ip_management_wireless` | `load_ip_management_submenu(..., '10001')` | 무선 IP |
| `ip_management_wired` | `load_ip_management_submenu(..., '10000')` | 유선 IP |
| `ip_management_ipphone` | `load_ip_management_submenu(..., '10002')` | 전화기 IP |
| `ip_management_server` | `load_ip_management_submenu(..., '10003')` | 서버 IP |
| `ip_management_hci` | `load_ip_management_submenu(..., '10004')` | HCI IP |
| `phone_management` | `load_phone_management` | 전화번호 관리 |
| `switch_backup` | `load_switch_backup_management` | 스위치 백업 관리 |
| `switch_port_mode` | `load_switch_port_mode_management` | 스위치 포트 정보 관리 |
| `log_management` | `load_log_management` | 전체 LOG 관리 |
| `ip_log` | `load_log_management_submenu(..., 'IP_MNG')` | IP LOG |
| `phone_log` | `load_log_management_submenu(..., 'PHN_MNG')` | 전화번호 LOG |
| `account_management` | `load_account_management` | 계정 관리 |

기존 `static/contents/*.html` 파일도 존재하지만 현재 주요 화면은 JS에서 동적으로 생성하는 구조가 중심이다.

---

## 7. 공통 테이블 기능

다수 화면은 `initializer.js`, `tableManager.js`, `searchManager.js`가 제공하는 공통 테이블 UI를 사용한다.

### 7.1 공통 검색 영역

대부분의 관리 화면에는 다음 UI가 있다.

- 일반 검색 입력창
- 일반 검색 버튼
- 하이라이트 검색 입력창
- 하이라이트 검색 버튼
- 상세 버튼
- 일괄 수정 버튼
- 일괄 삭제 버튼
- 페이지당 항목 수 선택
- 그룹/대역 선택 필터
- Excel 내려받기 버튼

화면에 따라 일부 버튼은 숨김 처리된다.

### 7.2 일반 검색

파일: `static/js/searchManager.js`

- 검색어를 소문자 처리한다.
- `:`, `-`, 공백을 제거한 문자열로 비교한다.
- 각 row의 모든 값 중 검색어가 포함된 값이 있으면 표시한다.
- 검색 실행 시 페이지는 1페이지로 초기화된다.
- 퇴사 사원 필터 상태도 초기화된다.

### 7.3 하이라이트 검색

- 현재 렌더링된 테이블 행 중 검색어를 포함하는 행에 `highlight-search` 클래스를 부여한다.
- 일반 검색처럼 행을 줄이는 것이 아니라 표시된 행에 색상을 강조하는 방식이다.

### 7.4 상세 검색/필터 영역

상세 버튼을 누르면 `advancedSearchContainer`가 열리고 닫힌다.

상세 영역에 포함될 수 있는 요소:

- 퇴사 사원 조회 버튼
- 항목 수 선택: 100, 200, 500, 전체
- 대역/그룹 선택
- Excel 내려받기 버튼

### 7.5 페이지네이션

공통 페이지네이션 버튼:

- 처음 페이지: `«`
- 이전 페이지: `‹`
- 현재 페이지 표시: `1 / N`
- 다음 페이지: `›`
- 마지막 페이지: `»`

동작:

- 기본 행 수는 100개이다.
- 항목 수를 전체로 선택하면 모든 데이터를 표시한다.
- 페이지 이동 시 테이블 상단으로 스크롤한다.
- 전체 선택 체크박스 상태는 페이지 이동/갱신 시 초기화된다.

### 7.6 정렬

- 테이블 헤더 클릭 시 해당 컬럼 기준 오름차순/내림차순 정렬을 토글한다.
- 숫자로 해석 가능한 값은 숫자 비교, 그 외는 문자열 비교를 사용한다.

### 7.7 전체 선택/일괄 선택

- 테이블 헤더의 체크박스로 현재 표시된 row의 체크박스를 전체 선택/해제한다.
- 각 행 체크 상태에 따라 전체 선택 체크박스 상태도 갱신된다.

---

## 8. IP 관리 기능

### 8.1 화면 종류

IP 메뉴는 통합 화면과 하위 분류 화면으로 구성된다.

| 화면 | 조건/분류 |
|---|---|
| IP 통합 관리 | 전체 IP 데이터 |
| 무선 IP | `PARENT_ID = '10001'` |
| 유선 IP | `PARENT_ID = '10000'` |
| 전화기 IP | `PARENT_ID = '10002'` |
| 서버 IP | `PARENT_ID = '10003'` |
| HCI IP | `PARENT_ID = '10004'` |
| 기타 IP | `PARENT_ID = '10005'`, 현재 메뉴는 주석 처리 |

### 8.2 데이터 조회

Frontend:

- `fetchIpData()` 호출
- API: `/it_mng/get_ip_data/`

Backend:

- `get_ip_data`가 Raw SQL로 여러 테이블을 조인한다.
- 반환 JSON 키: `ip_data`

조회에 포함되는 주요 정보:

- IP ID
- IP 주소
- 회사명
- 사용자명 또는 기타 사용자명
- 사용 여부
- 전화번호
- 전화 목적
- IPScan 이름/사용자
- 부서
- IPScan 장비 구분
- IP 비고
- MAC
- 장비 비고
- 사용자 ID
- IP 그룹 상위 ID
- 그룹 ID
- 그룹명

관련 테이블/뷰:

- `IP_MNG`
- `IP_GRP_INF`
- `IP_PRN_INF`
- `USR_INF`
- `OTH_INF`
- `NTWR_DVCS_INF`
- `DPT_INF`
- `CPY_INF`
- `PHN_MNG`

### 8.3 IP 테이블 컬럼

Frontend 테이블 헤더 기준:

1. 선택 체크박스
2. INDEX
3. IP
4. 삭제 버튼
5. MAC
6. 회사
7. 이름
8. IPScan이름
9. 부서
10. IPScan부서
11. 비고
12. 전화번호

### 8.4 IP 단건 수정

진입:

- IP 컬럼의 IP 버튼 클릭
- `ip_management_handlePopupOpen` 실행

팝업 필드:

- IP: 표시 전용
- 이름: contenteditable 입력/사용자 선택 영역
- 비고: textarea
- 사용자 ID: hidden input

사용자 선택 방식:

- 이름 입력 후 Enter로 검색
- 사용자 후보 드롭다운 표시
- 방향키/마우스로 선택 가능
- 선택한 사용자는 `회사 - 이름 (부서)` 형태의 사용자 블록으로 표시
- 사용자 블록의 X 버튼으로 선택 해제 가능

저장:

- API: `/it_mng/update_ip/`
- Method: POST
- Body: `ip_id`, `user_id`, `note`

Backend 동작:

- `IP_MNG`의 해당 `IP_ID`를 조회한다.
- `USER_ID`, `NOTE`를 업데이트한다.
- `user_view`에서 사용자 표시 정보를 다시 조회한다.
- 성공 시 갱신된 사용자/부서/회사/비고 데이터를 반환한다.

Frontend 반영:

- 성공 시 새로고침 없이 해당 행의 회사, 이름, 부서, 비고를 즉시 갱신한다.
- 삭제 버튼 disabled 상태를 해제한다.

### 8.5 IP 단건 삭제

진입:

- IP 행의 `x` 삭제 버튼 클릭

확인 메시지:

- `{IP주소}에 등록된 정보를 삭제하시겠습니까?`

API:

- `/it_mng/delete_ip/`
- Method: POST
- Body: `ip_id`, `user_id: ''`, `note: ''`

Backend 동작:

- 실제 row 삭제가 아니라 `IP_MNG`의 `USER_ID`, `NOTE`를 빈 값으로 갱신한다.

Frontend 반영:

- 해당 행의 회사, 이름, 부서, 비고를 빈 값으로 바꾼다.
- 삭제 버튼을 disabled 처리한다.

### 8.6 IP 일괄 수정

진입:

- 행 체크박스로 여러 IP 선택
- `일괄 수정` 버튼 클릭

팝업 표시:

- 선택된 IP 목록
- 현재 이름
- 현재 비고
- 공통으로 적용할 사용자
- 공통으로 적용할 비고

API:

- `/it_mng/bulk_update_ip/`
- Method: POST
- Body: `ip_ids`, `user_id`, `note`

Backend 동작:

- 선택된 IP ID 목록을 순회하며 `USER_ID`, `NOTE`를 업데이트한다.
- 공통 사용자 정보를 `user_view`에서 조회하여 반환한다.

Frontend 반영:

- 선택된 모든 행에 동일 사용자/부서/회사/비고를 즉시 반영한다.
- 체크박스 선택을 해제한다.

### 8.7 IP 일괄 삭제

진입:

- 행 체크박스로 여러 IP 선택
- `일괄 삭제` 버튼 클릭

확인 메시지:

- `선택한 N개의 IP를 삭제하시겠습니까?`

API:

- `/it_mng/bulk_delete_ip/`
- Method: POST
- Body: `ip_ids`, `user_id: ''`, `note: ''`

Backend 동작:

- 선택된 IP들의 `USER_ID`, `NOTE`를 빈 값으로 업데이트한다.

Frontend 반영:

- 선택된 행들의 회사, 이름, 부서, 비고를 빈 값으로 변경한다.
- 삭제 버튼 disabled 처리
- 체크박스 선택 해제

### 8.8 전화기 IP 화면 특이점

`ip_management_ipphone` 화면에서는 IP 수정/삭제 계열 UI가 제한된다.

- IP 버튼이 disabled 처리된다.
- 일괄 수정/삭제 버튼이 숨김 처리된다.

전화기 IP는 전화번호 관리 화면에서 IP를 연결하는 후보로 사용하는 성격이 강하다.

---

## 9. 전화번호 관리 기능

### 9.1 데이터 조회

Frontend:

- `fetchPhoneData()` 호출
- API: `/it_mng/phone_management/`

Backend:

- `phone_management`가 Raw SQL로 전화번호, IP, 사용자, 부서, 회사, IPScan 정보를 조합한다.
- 반환 JSON 키: `phone_data`

주요 조회 항목:

- 전화번호
- 시작일/종료일
- 사용자명 또는 기타 사용자명
- IPScan 이름
- 부서
- 회사
- 사용 여부
- 목적
- 비고
- IP
- MAC
- 사용자 ID
- IP ID

관련 테이블:

- `PHN_MNG`
- `IP_MNG`
- `USR_INF`
- `OTH_INF`
- `NTWR_DVCS_INF`
- `DPT_INF`
- `CPY_INF`

### 9.2 전화번호 테이블 컬럼

1. 선택 체크박스
2. INDEX
3. 내선번호
4. 삭제 버튼
5. 회사
6. 이름
7. IPSCAN 이름
8. 부서
9. 목적
10. 비고
11. 전화기 IP
12. 전화기 MAC

### 9.3 전화번호 단건 수정

진입:

- 내선번호 버튼 클릭

팝업 필드:

- 전화번호: 표시 전용
- 이름: 사용자 검색/선택
- 목적: textarea, 기본값은 기존 값 또는 `내선전화`
- 비고: textarea
- IP: `IP 선택` 클릭 영역
- IP ID: hidden input

저장 API:

- `/it_mng/update_phone/`
- Method: POST
- Body: `phone_id`, `user_id`, `purpose`, `note`, `ip_id`

Backend 동작:

- 트랜잭션으로 처리한다.
- `PHN_MNG`에서 해당 전화번호의 사용자, 목적, 비고, IP ID를 갱신한다.
- 새 IP ID가 있으면 `IP_MNG`의 해당 IP에도 `USER_ID`, `NOTE`를 반영한다.
- 기존 IP ID가 있고 새 IP ID와 다르면 기존 IP의 `USER_ID`, `NOTE`를 빈 값으로 정리한다.
- 사용자/IP/MAC 정보를 다시 조회해 반환한다.

Frontend 반영:

- 성공 시 해당 전화번호 행의 회사, 이름, 부서, 목적, 비고, IP, MAC을 즉시 갱신한다.
- 삭제 버튼 disabled 상태를 해제한다.

### 9.4 전화번호 단건 삭제

진입:

- 전화번호 행의 `x` 삭제 버튼 클릭

API:

- `/it_mng/delete_phone/`
- Method: POST
- Body: `phone_id`, `user_id: ''`, `purpose: ''`, `note: ''`, `ip_id`

Backend 동작:

- 트랜잭션으로 처리한다.
- `PHN_MNG`에서 사용자, 목적, 비고를 빈 값으로 갱신하고 IP ID를 빈 값으로 만든다.
- 연결되어 있던 IP가 있으면 `IP_MNG`의 `USER_ID`, `NOTE`도 빈 값으로 정리한다.

Frontend 반영:

- 전화번호 행의 회사, 이름, 부서, 목적, 비고, IP, MAC을 빈 값으로 변경한다.
- 삭제 버튼 disabled 처리

### 9.5 전화번호 일괄 수정

진입:

- 여러 전화번호 행 선택
- `일괄 수정` 클릭

팝업 표시:

- 선택된 전화번호 목록
- 현재 이름
- 현재 목적
- 현재 비고
- 현재 IP
- 공통 사용자
- 공통 목적
- 공통 비고
- 각 전화번호별 IP 선택 가능

IP 선택:

- 일괄 수정 팝업 안의 각 IP 영역을 클릭하면 IP 선택 모달이 열린다.
- 선택된 IP는 해당 전화번호에 개별 적용된다.

API:

- `/it_mng/bulk_update_phone/`
- Method: POST
- Body: `updates` 배열
  - 각 원소: `phone_id`, `ip_id`, `user_id`, `note`, `purpose`

Backend 동작:

- 트랜잭션으로 여러 전화번호를 순회 업데이트한다.
- 각 전화번호의 기존 IP와 새 IP를 비교한다.
- 새 IP가 있으면 `IP_MNG`에도 사용자/비고를 반영한다.
- 기존 IP가 비워졌으면 기존 IP의 사용자/비고를 정리한다.
- 공통 사용자 정보와 IP/MAC 정보를 병합해 반환한다.

Frontend 반영:

- 반환된 배열을 기준으로 여러 전화번호 행을 즉시 갱신한다.
- 체크박스 선택 해제

### 9.6 전화번호 일괄 삭제

진입:

- 여러 전화번호 선택
- `일괄 삭제` 클릭

API:

- `/it_mng/bulk_delete_phone/`
- Method: POST
- Body: `phone_ids`, `ip_ids`, `user_id: ''`, `purpose: ''`, `note: ''`

Backend 동작:

- `PHN_MNG`의 선택된 전화번호 사용자/목적/비고/IP ID를 빈 값으로 갱신한다.
- 선택된 IP ID들의 `IP_MNG.USER_ID`, `IP_MNG.NOTE`를 빈 값으로 갱신한다.

Frontend 반영:

- 선택된 전화번호 행의 사용자/목적/비고/IP/MAC 정보를 빈 값으로 갱신한다.
- 체크박스 선택 해제

### 9.7 전화번호용 IP 선택 모달

모달 ID: `ipSelectionModal`

데이터 API:

- `/it_mng/phone_ip_data/`

Backend 조건:

- `IP_MNG.GROUP_ID IN ('10020', '10016')`
- 전화기 관련 IP 대역 후보로 보인다.

모달 기능:

- IP 주소 검색
- 대역 선택 select
- IP/설명 테이블 표시
- 이미 사용자명이 있는 IP는 disabled 처리
- 일괄 수정 중 이미 선택된 IP도 disabled 처리
- 사용 가능한 IP 클릭 시 선택되고 모달이 닫힌다.
- 선택된 IP 옆 X 버튼으로 IP 선택 해제 가능

---

## 10. 사용자 검색/선택 기능

### 10.1 전체 사용자 목록 조회

API:

- `/it_mng/get_user_data/`

Backend:

- `get_user_info` 함수에서 Raw SQL 실행
- `USR_INF`와 `OTH_INF`를 UNION하여 통합 사용자 목록을 만든다.
- 부서명과 회사명을 조인한다.

반환 필드:

- `USER_ID`
- `USER_NAME`
- `DEPT_NAME`
- `CPY_NAME`
- `USE_YN`

### 10.2 이름 검색 방식

Frontend는 실제 팝업 사용자 검색에서 `/it_mng/search_users/`보다는 `fetchUserData()` 전체 목록을 받은 뒤 클라이언트에서 이름 포함 검색을 수행한다.

동작:

- 이름 입력 후 Enter
- 사용자 목록 중 `USER_NAME`에 검색어가 포함된 항목 필터링
- 드롭다운으로 후보 표시
- 퇴사/비활성 사용자는 `USE_YN === 'N'`이면 inactive 클래스로 표시

### 10.3 키보드 조작

- Enter: 검색 실행 또는 선택된 후보 확정
- ArrowDown: 다음 후보 이동
- ArrowUp: 이전 후보 이동
- Escape: 드롭다운 닫기

---

## 11. LOG 관리 기능

### 11.1 데이터 조회

API:

- `/it_mng/log_data/`

Backend:

- `CHANGE_LOG` 테이블 전체 조회
- `LOG_ID DESC` 정렬
- 반환 JSON 키: `log_data`

### 11.2 전체 LOG 화면

메뉴:

- LOG 클릭 시 `LOG 관리` 화면 표시

테이블 컬럼:

1. 선택 영역
2. 날짜
3. 시간
4. 필드
5. 컬럼
6. 변경 값
7. 기존 값

### 11.3 IP LOG / 전화번호 LOG

하위 메뉴:

- IP LOG
  - `table_name === 'IP_MNG'` 필터
- 전화번호 LOG
  - `table_name === 'PHN_MNG'` 필터

### 11.4 LOG 테이블 표시 방식

`logRowTemplate`은 같은 변경 묶음을 보기 쉽게 표시하기 위해 일부 셀에 rowspan을 사용한다.

묶음 기준:

- `row_name`
- `change_date`
- `change_time`

같은 변경 묶음에서는 날짜/시간/필드 셀을 rowspan으로 병합한다.

---

## 12. 스위치 포트 정보 관리

### 12.1 데이터 조회

API:

- `/it_mng/switch_port_mode_data/`

Backend:

- `switch_port_mode_data`에서 Raw SQL 실행
- 스위치, 랙, 포트 모드, 포트 위치, MAC, 사용자 IP, 사용자/부서/회사, 전화번호를 조합한다.
- `ETH_SWT_INF`는 `INTERFACE`, `SWITCH_ID` 기준으로 `ROW_NUMBER()`를 사용해 상위 3개 MAC만 조인한다.

관련 테이블:

- `RCK_INF`
- `SWT_INF`
- `SWT_PRT_MD_INF`
- `PRT_CNC_LCT_INF`
- `ETH_SWT_INF`
- `NTWR_DVCS_INF`
- `IP_MNG`
- `USR_INF`
- `OTH_INF`
- `DPT_INF`
- `CPY_INF`
- `PHN_MNG`

### 12.2 화면 기능

메뉴:

- 스위치 > 스위치 포트 정보

테이블 컬럼:

1. 포트 번호 또는 선택 영역 위치
2. RACK
3. SWITCH IP
4. PORT
5. PORT MODE
6. 아웃렛
7. VLAN
8. IP
9. MAC
10. 사용자
11. 부서
12. 회사
13. 비고
14. 전화번호

### 12.3 필터/검색

- 공통 검색 가능
- 상세 영역에서 스위치 IP select 필터 제공
- 항목 수 선택 가능
- Excel 다운로드 가능
- 수정/삭제 기능은 제공하지 않는다.

### 12.4 Excel 다운로드

API:

- `/it_mng/export_switch_port_mode_data/`

컬럼명 매핑:

| 원본 필드 | Excel 컬럼 |
|---|---|
| `RACK_NAME` | RACK |
| `SWITCH_IP` | 스위치 IP |
| `INTERFACE` | 포트 |
| `PORT_MODE` | 포트 모드 |
| `AREA_NUMBER` | 아웃렛 |
| `VLAN` | VLAN |
| `USER_IP` | IP |
| `USER_MAC` | MAC |
| `USER_NAME` | 이름 |
| `DEPT_NAME` | 부서 |
| `CPY_NAME` | 회사 |
| `NOTE` | 비고 |
| `PHONE_ID` | 전화번호 |

파일명:

- `스위치포트정보_YYYYMMDDHHMMSS.xlsx`

---

## 13. 스위치 백업 관리

### 13.1 데이터 조회

API:

- `/it_mng/switch_backup_data/`

Backend:

- `switch_backup_data`에서 Raw SQL 실행
- 랙, 스위치 IP, 설정 백업 데이터, 백업 상태, 백업 날짜/시간, 스위치 정렬값을 조회한다.

관련 테이블:

- `RCK_INF`
- `SWT_INF`
- `SWT_CNF_BCK`
- `SWT_BCK_INF`

반환 JSON 키:

- `switch_backup_data`

### 13.2 화면 구성

메뉴:

- 스위치 > 스위치 백업

화면은 3개 패널로 구성된다.

1. 백업 목록
   - 날짜
   - 시간
   - 전체 다운로드 버튼
2. 스위치 목록
   - 렉
   - 스위치 IP
   - 렉 단위 다운로드 버튼
3. 백업 데이터
   - 선택한 스위치 설정 내용 textarea 표시
   - 복사 버튼
   - 다운로드 버튼

### 13.3 사용 흐름

1. 스위치 백업 메뉴 진입
2. 백업 날짜/시간 목록 로딩
3. 날짜/시간 row 클릭
4. 해당 백업 시점의 렉/스위치 목록 표시
5. 스위치 row 클릭
6. 설정 백업 텍스트 표시
7. 필요 시 복사 또는 다운로드

### 13.4 전체 백업 다운로드

API:

- `/it_mng/switch_backup_download/datetime/`
- Method: POST
- 로그인 필요

Body:

- `backup_date`
- `backup_time`

결과:

- ZIP 파일 다운로드
- ZIP 내부 폴더 구조:
  - `{date}-{time}/{rack}/{ip}-{date}.txt`

### 13.5 렉 단위 다운로드

API:

- `/it_mng/switch_backup_download/rack/`
- Method: POST
- 로그인 필요

Body:

- `backup_date`
- `backup_time`
- `rack_name`

결과:

- ZIP 파일 다운로드
- ZIP 내부 폴더 구조:
  - `{rack}/{ip}-{date}.txt`

### 13.6 단건 스위치 설정 다운로드

API:

- `/it_mng/switch_backup_download/single/`
- Method: POST
- 로그인 필요

Body:

- `backup_date`
- `backup_time`
- `backup_switch_ip`

결과:

- TXT 파일 다운로드
- 파일명:
  - `{backup_switch_ip}-{backup_date}.txt`

### 13.7 설정 복사

Frontend:

- `navigator.clipboard.writeText`를 우선 사용한다.
- 실패 시 textarea select + `document.execCommand('copy')` fallback을 사용한다.
- 성공/실패 상황은 toast 메시지로 표시된다.

---

## 14. Excel 다운로드 기능

### 14.1 IP/전화번호 Excel 다운로드

API:

- `/it_mng/export_ip_data/`

Frontend:

- 현재 화면의 전체 data 배열을 POST body로 전달한다.
- 파일명은 화면에 따라 다르다.
  - IP: `IP정보_YYYYMMDDHHMMSS.xlsx`
  - 전화번호: `전화번호정보_YYYYMMDDHHMMSS.xlsx`

Backend:

- pandas DataFrame 생성
- 화면 종류에 따라 컬럼 매핑
- openpyxl로 Excel 생성
- 헤더 bold 처리
- 셀 가운데 정렬
- 열 너비 자동 조정

IP 다운로드 컬럼:

| 원본 필드 | Excel 컬럼 |
|---|---|
| `IP` | IP |
| `EXCEL_NAME` | 이름 |
| `EXCEL_DEPT` | 부서 |
| `LOG_NOTE` | 비고 |
| `DEVICE_MAC` | MAC |
| `GROUP_NAME` | 그룹 |

전화번호 다운로드 컬럼:

| 원본 필드 | Excel 컬럼 |
|---|---|
| `PHONE_ID` | 전화번호 |
| `CPY_NAME` | 회사 |
| `NAME` | 이름 |
| `DEPT_NAME` | 부서 |
| `PURPOSE` | 목적 |
| `IP` | IP |
| `NOTE` | 비고 |
| `MAC` | MAC |

### 14.2 스위치 포트 Excel 다운로드

자세한 내용은 12.4 참고.

---

## 15. 데이터 업데이트 버튼 기능

헤더의 3개 버튼은 외부 Python 스크립트를 실행해 데이터를 갱신하는 기능이다.

### 15.1 IP 데이터 업데이트

버튼:

- `IP 데이터 업데이트`

API:

- `/it_mng/ipscan_data_update/`

실행 스크립트:

- `IT_MNG_SITE/script/ipscsan_data_extraction.py`

응답 메시지:

- 성공: `IP 데이터 불러오기 성공`
- 실패: `IP 데이터 불러오기 실패`

비고:

- 코드 주석에 따르면 IPScan이 사용하는 MariaDB 버전이 낮아 기능 문제 가능성이 언급되어 있다.

### 15.2 GW 데이터 업데이트

버튼:

- `GW 데이터 업데이트`

API:

- `/it_mng/gw_data_update/`

실행 스크립트:

- `IT_MNG_SITE/script/gw_all_data_extraction.py`

응답 메시지:

- 성공: `GW 데이터 불러오기 성공`
- 실패: `GW 데이터 불러오기 실패`

### 15.3 스위치 포트 데이터 업데이트

버튼:

- `스위치 포트 데이터 업데이트`

API:

- `/it_mng/switch_port_data_update/`

실행 스크립트:

- `IT_MNG_SITE/script/eth_switch_mode_extraction.py`

응답 메시지:

- 성공: `스위치 포트 정보 불러오기 성공`
- 실패: `스위치 포트 정보 불러오기 실패`

### 15.4 Frontend 공통 동작

- 버튼 클릭 시 전체화면 로딩 오버레이 표시
- POST 요청 실행
- 응답의 `message`를 alert로 표시
- 완료 후 로딩 오버레이 숨김

---

## 16. 계정 관리 기능

### 16.1 접근 조건

- 화면 메뉴는 staff 사용자에게만 표시된다.
- API도 `@staff_member_required`가 적용되어 staff 사용자만 접근 가능하다.

### 16.2 계정 목록 조회

API:

- `/it_mng/user_list_api/`

Backend:

- Django `User` 모델에서 다음 필드 조회
  - `id`
  - `username`
  - `is_active`
  - `is_staff`

Frontend 화면 컬럼:

1. No
2. 아이디
3. 권한
   - `관리자` 또는 `일반`
4. 사용여부
   - `활성` 또는 `비활성`
5. 관리
   - 사용자 정보 수정 버튼

### 16.3 계정 생성

진입:

- `계정 생성` 버튼 클릭

팝업 필드:

- 관리자 계정 체크박스
- 아이디
- 비밀번호
- 비밀번호 확인

API:

- `/it_mng/users/create/`
- Method: POST

Body:

- `username`
- `password1`
- `password2`
- `is_staff`

Backend 검증:

- 비밀번호 일치 여부 확인
- username 중복 확인
- Django password validator 적용

성공 시:

- User 생성
- `is_active = True`
- `is_staff`는 체크박스 값 반영

### 16.4 계정 수정

진입:

- 사용자 정보 수정 버튼 클릭

팝업 필드:

- 관리자 권한 체크박스
- 계정 활성 체크박스
- 새 비밀번호
- 비밀번호 확인

API:

- `/it_mng/users/update/`
- Method: POST

Body:

- `user_id`
- `is_staff`
- `is_active`
- `password1`
- `password2`

Backend 동작:

- 대상 User 조회
- 본인 계정은 수정 불가
- 관리자 여부/활성 여부 갱신
- 비밀번호 입력 시 `SetPasswordForm`으로 검증 후 변경

성공 시:

- 계정 목록 재조회/렌더링

---

## 17. 테마 기능

파일:

- `static/js/themeHandler.js`
- `static/css/home/variables.css`
- `static/css/home/theme.css`

### 17.1 제공 테마

| ID | 표시 이름 |
|---|---|
| `default` | Pastel Slate |
| `pastel-blue` | Pastel Blue |
| `pastel-mint` | Pastel Mint |
| `pastel-lavender` | Pastel Lavender |
| `original` | Original Navy |

### 17.2 동작 방식

- 페이지 로드 시 localStorage의 `app_theme` 값을 읽는다.
- 선택한 테마 ID를 `document.documentElement`의 `data-theme` 속성에 적용한다.
- `default`는 `data-theme` 속성을 제거한다.
- 헤더 우측에 팔레트 버튼과 드롭다운을 JS로 삽입한다.
- 테마 선택 값은 localStorage에 저장되어 다음 접속 시 복원된다.

### 17.3 CSS 구조

`variables.css`에 CSS 변수 기반 색상/그림자/반경 값이 정의되어 있고, 테마별로 변수 값을 덮어쓴다.

---

## 18. 공통 Modal/UX 기능

### 18.1 모달 종류

`home.html`에 다음 모달이 미리 정의되어 있다.

- IP 정보 수정 모달: `popupModal`
- 전화번호 정보 수정 모달: `phone_popupModal`
- IP 선택 모달: `ipSelectionModal`
- 계정 생성 모달: `createaccount_popupModal`
- 계정 수정 모달: `updateaccount_popupModal`
- 로딩 화면: `loadingScreen`

### 18.2 모달 드래그

파일: `popupHandler.js`

- `initDraggableModal` 함수로 모달 타이틀 영역을 잡고 이동할 수 있다.
- IP/전화번호/계정/선택 모달에 적용된다.

### 18.3 Toast 메시지

스위치 백업 다운로드/복사 기능에서 toast 메시지를 사용한다.

예:

- 다운로드 준비 중...
- 다운로드 완료!
- 다운로드 실패
- 클립보드에 복사되었습니다.

### 18.4 Loading UI

두 종류가 있다.

1. 콘텐츠 영역 로딩
   - `.main-content` 안에 spinner 표시
   - 메뉴별 데이터 로딩 시 사용
2. 전체화면 로딩
   - 데이터 업데이트 버튼 실행 시 사용
   - 반투명 overlay + spinner + `데이터 불러오는 중...`

---

## 19. Django 모델/DB 매핑

파일: `it_mng/models.py`

### 19.1 모델 목록

| Django 모델 | DB 테이블/뷰 | 설명 |
|---|---|---|
| `IPManagement` | `IP_MNG` | IP 관리 원본 테이블 |
| `PhoneManagement` | `PHN_MNG` | 전화번호 관리 테이블 |
| `DepartmentInfo` | `DPT_INF` | 부서 정보 |
| `UserInfo` | `USR_INF` | 사용자 정보 |
| `OtherInfo` | `OTH_INF` | 기타 사용자/외부 사용자 정보 |
| `NetworkDeviceInfo` | `NTWR_DVCS_INF` | IPScan/네트워크 장비 정보 |
| `CompanyInfo` | `CPY_INF` | 회사 정보 |
| `PortConnectLocationInfo` | `PRT_CNC_LCT_INF` | 포트 연결 위치 정보 |
| `IpMngVw` | `ipmng_vwtbl` | IP 관리 조회용 DB View, managed=False |

### 19.2 핵심 데이터 관계

#### IP 중심

- `IP_MNG.USER_ID`는 `USR_INF.USER_ID` 또는 `OTH_INF.OTHER_ID`와 연결된다.
- `IP_MNG.GROUP_ID`는 IP 그룹 테이블과 연결된다.
- `IP_MNG.IP_ID`는 `NTWR_DVCS_INF.IP_ID`와 연결되어 MAC/장비명/IPScan 정보를 가져온다.
- `PHN_MNG.IP_ID`는 전화번호가 사용하는 IP와 연결된다.

#### 전화번호 중심

- `PHN_MNG.USER_ID`는 사용자/기타 사용자와 연결된다.
- `PHN_MNG.IP_ID`는 `IP_MNG.IP_ID`와 연결된다.
- 전화번호 수정 시 `PHN_MNG`뿐 아니라 연결된 `IP_MNG`도 같이 갱신된다.

#### 스위치 포트 중심

- `RCK_INF` → `SWT_INF` → `SWT_PRT_MD_INF` 흐름으로 랙/스위치/포트 정보를 가져온다.
- `PRT_CNC_LCT_INF`로 포트의 아웃렛/위치 정보를 연결한다.
- `ETH_SWT_INF`의 MAC을 `NTWR_DVCS_INF.MAC`과 연결해 사용자 IP를 추적한다.
- 사용자 IP를 다시 `IP_MNG`, `USR_INF`, `OTH_INF`, `PHN_MNG`와 연결해 사용자/전화번호 정보를 표시한다.

---

## 20. 화면별 데이터 흐름 요약

### 20.1 IP 관리

1. 사이드바 IP 메뉴 클릭
2. `loadContent('ip_management')`
3. `load_ip_management`
4. `fetchIpData`
5. `/it_mng/get_ip_data/`
6. Raw SQL로 IP/사용자/IPScan/전화번호 정보 조회
7. 테이블 렌더링
8. 검색/필터/페이지네이션/Excel/수정/삭제 이벤트 연결

### 20.2 IP 하위 분류

1. 무선/유선/IP Phone/Server/HCI 메뉴 클릭
2. 전체 IP 데이터 조회
3. `PARENT_ID` 기준으로 클라이언트 필터링
4. 테이블 렌더링

### 20.3 전화번호 관리

1. 전화번호 메뉴 클릭
2. `load_phone_management`
3. `/it_mng/phone_management/`
4. Raw SQL로 전화번호/사용자/IP/MAC 정보 조회
5. 테이블 렌더링
6. 수정 시 사용자 검색 및 IP 선택 모달 사용
7. 저장 시 전화번호 테이블과 IP 테이블 동시 갱신

### 20.4 LOG 관리

1. LOG 메뉴 클릭
2. `/it_mng/log_data/`
3. CHANGE_LOG 전체 조회
4. 전체 또는 테이블명 기준 필터링
5. rowspan 기반 테이블 렌더링

### 20.5 스위치 포트 정보

1. 스위치 > 스위치 포트 정보 클릭
2. `/it_mng/switch_port_mode_data/`
3. 랙/스위치/포트/MAC/IP/사용자 정보 조합 조회
4. 스위치 IP 필터와 Excel 다운로드 제공

### 20.6 스위치 백업

1. 스위치 > 스위치 백업 클릭
2. `/it_mng/switch_backup_data/`
3. 백업 날짜/시간 목록 구성
4. 날짜/시간 선택
5. 렉/스위치 목록 표시
6. 스위치 선택
7. 설정 텍스트 표시/복사/다운로드

### 20.7 계정 관리

1. staff 사용자로 로그인
2. 계정 관리 메뉴 클릭
3. `/it_mng/user_list_api/`
4. 계정 목록 렌더링
5. 계정 생성 또는 수정 API 호출
6. 성공 시 목록 재조회

---

## 21. 현재 코드상 존재하지만 UI에서 제한/미사용으로 보이는 요소

### 21.1 static/contents HTML

`static/contents/` 아래에 여러 HTML 조각 파일이 있다.

예:

- `ip_management.html`
- `phone_management.html`
- `switch_management.html`
- `log_management.html`
- `user_management.html`
- 하위 IP/LOG/스위치 관련 HTML 파일들

하지만 현재 `home.js`와 `initializer.js` 구조에서는 주요 화면을 fetch HTML이 아니라 JS 템플릿 문자열로 생성하고 있다.
따라서 이 파일들은 이전 구조의 잔재이거나 일부 미사용 파일일 가능성이 높다.

### 21.2 `get_ip_management_data`

- `IpMngVw` 기반 페이지네이션 API가 존재한다.
- 현재 주요 Frontend 흐름은 `/it_mng/get_ip_data/`를 사용한다.
- 새 UI 설계 시 서버사이드 페이지네이션이 필요하면 참고 가능하다.

### 21.3 `search_users`

- 사용자명 POST 검색 API가 존재한다.
- 현재 팝업 검색은 `/it_mng/get_user_data/` 전체 목록을 받은 뒤 클라이언트 검색하는 방식이다.
- 사용자 수가 많아지면 `search_users` 방식 또는 별도 서버 검색 API가 더 적합할 수 있다.

### 21.4 `update_ip_view`, `update_ip_data`

- 코드에 존재하지만 URL에 직접 연결되어 있지 않다.
- 현재 IP 수정은 `update_ip`가 담당한다.

---

## 22. 새 UI/구조 설계를 위한 기능 단위 정리

새 구조를 만들 때 기능을 다음 도메인으로 분리하면 적합하다.

### 22.1 Auth 도메인

- 로그인
- 로그아웃
- 현재 사용자 표시
- staff 권한 체크

### 22.2 Navigation/Layout 도메인

- 헤더
- 사이드바
- 콘텐츠 영역
- 로딩 overlay
- 테마 선택

### 22.3 IP Management 도메인

- IP 목록 조회
- IP 대역/그룹 필터
- IP 검색/하이라이트
- IP 단건 수정
- IP 단건 삭제
- IP 일괄 수정
- IP 일괄 삭제
- IP Excel 다운로드

### 22.4 Phone Management 도메인

- 전화번호 목록 조회
- 전화번호 검색/하이라이트
- 전화번호 단건 수정
- 전화번호 단건 삭제
- 전화번호 일괄 수정
- 전화번호 일괄 삭제
- 전화번호 Excel 다운로드
- 전화번호에 연결할 IP 선택

### 22.5 User Lookup 도메인

- 사용자/기타 사용자 통합 목록 조회
- 이름 검색
- 사용자 선택 컴포넌트
- 퇴사자 표시/필터

### 22.6 Switch Port 도메인

- 스위치 포트 목록 조회
- 스위치 IP 필터
- 검색/정렬/페이지네이션
- Excel 다운로드
- 외부 스위치 포트 데이터 갱신 실행

### 22.7 Switch Backup 도메인

- 백업 목록 조회
- 날짜/시간별 그룹핑
- 렉/스위치 목록 표시
- 설정 텍스트 표시
- 전체 ZIP 다운로드
- 렉 ZIP 다운로드
- 단건 TXT 다운로드
- 클립보드 복사

### 22.8 Log 도메인

- 전체 로그 조회
- IP 로그 필터
- 전화번호 로그 필터
- 변경 묶음 표시

### 22.9 Account Admin 도메인

- 계정 목록 조회
- 계정 생성
- 계정 권한 수정
- 계정 활성/비활성 수정
- 비밀번호 재설정

### 22.10 Data Sync 도메인

- IPScan 데이터 갱신
- 그룹웨어 데이터 갱신
- 스위치 포트 데이터 갱신
- 실행 중 로딩 표시
- 성공/실패 메시지 표시

---

## 23. API 응답 구조 요약

| API | 응답 키/형태 |
|---|---|
| `/get_ip_data/` | `{ ip_data: [...] }` |
| `/get-ip-management_data/` | `{ data, page, total_pages, total_items }` |
| `/get_user_data/` | `{ users: [...] }` |
| `/update_ip/` | `{ success, updatedData }` 또는 `{ success:false, message }` |
| `/delete_ip/` | `{ success }` 또는 `{ success:false, message }` |
| `/bulk_update_ip/` | `{ success, bulkUpdatedData, message }` |
| `/bulk_delete_ip/` | `{ success, message }` |
| `/phone_management/` | `{ phone_data: [...] }` |
| `/phone_ip_data/` | `{ phone_ip_data: [...] }` |
| `/update_phone/` | `{ success, PhoneUpdatedData }` |
| `/delete_phone/` | `{ success }` |
| `/bulk_update_phone/` | `{ success, PhoneUpdatedData: [...], message }` |
| `/bulk_delete_phone/` | `{ success }` |
| `/log_data/` | `{ log_data: [...] }` |
| `/switch_port_mode_data/` | `{ switch_port_mode_data: [...] }` |
| `/switch_backup_data/` | `{ switch_backup_data: [...] }` |
| `/ipscan_data_update/` | `{ message, output/error }` |
| `/gw_data_update/` | `{ message, output/error }` |
| `/switch_port_data_update/` | `{ message, output/error, returncode?, stdout? }` |
| `/user_list_api/` | `{ user_list_api: [...] }` |
| `/users/create/` | `{ result:'success' }` 또는 `{ error }` |
| `/users/update/` | `{ result:'success' }` 또는 `{ error }` |

---

## 24. 주의할 점/개선 참고사항

이 항목은 코드 수정이 아니라, 새 UI/구조 설계 시 참고할 관찰 사항이다.

### 24.1 Frontend가 전체 데이터를 많이 가져오는 구조

- IP, 전화번호, 로그, 스위치 포트는 전체 데이터를 가져와 클라이언트에서 검색/필터/페이지네이션한다.
- 데이터가 커지면 초기 로딩이 느려질 수 있다.
- 새 구조에서는 서버사이드 검색/필터/페이지네이션 API를 고려할 수 있다.

### 24.2 기능별 관심사가 혼재되어 있음

- `initializer.js`가 화면 HTML 생성, 이벤트 연결, 다운로드, 스위치 백업 렌더링, 계정 관리까지 담당한다.
- `popupHandler.js`가 IP, 전화번호, 사용자 검색, IP 선택, 계정 팝업을 모두 담당한다.
- 새 UI에서는 도메인별 컴포넌트/서비스 분리가 좋다.

### 24.3 CSRF 처리 방식이 혼재

- 일부 API는 `@csrf_exempt`가 적용되어 있다.
- 스위치 백업 다운로드는 CSRF 토큰을 header에 넣는 구조이다.
- 새 구조에서는 CSRF 정책을 일관되게 설계하는 것이 좋다.

### 24.4 실제 삭제가 아닌 값 초기화

- IP 삭제/전화번호 삭제는 DB row를 삭제하는 것이 아니라 주요 필드를 빈 값으로 업데이트한다.
- 사용자 입장에서는 “등록 해제” 또는 “할당 해제”에 더 가까운 동작이다.
- 새 UI 문구에서 삭제보다 “등록 해제”라고 표현하는 것이 오해를 줄일 수 있다.

### 24.5 전화번호 수정은 IP 데이터도 함께 변경함

- 전화번호에 IP를 연결/변경하면 `PHN_MNG`뿐 아니라 `IP_MNG`도 함께 갱신된다.
- 기존 IP 연결이 변경되면 기존 IP의 사용자/비고를 비운다.
- 새 구조에서 이 연동 규칙을 명확히 표현해야 한다.

### 24.6 미사용/잔재 파일 가능성

- `static/contents/*.html`은 현재 JS 동적 렌더링 구조와 중복된다.
- `home_back.js`, `popupHandler_sub.js`, `popupHandler copy.js`, `login copy.html`, `login copy.css` 등 백업/복사본 성격 파일이 있다.
- 새 구조 설계 시 실제 사용 파일과 잔재 파일을 분리해 판단해야 한다.

### 24.7 관리자 계정 수정 보호

- Backend에서 본인 계정 수정은 막고 있다.
- 새 UI에서도 본인 계정 수정 버튼 비활성화 또는 안내 메시지를 제공하면 좋다.

### 24.8 외부 스크립트 실행 시간

- 스위치 포트 데이터 수집은 주석/업데이트 내역상 10초 이상 걸릴 수 있다.
- 새 UI에서는 진행 상태, 비동기 작업 큐, 실행 로그 표시를 고려할 수 있다.

---

## 25. 새 UI 설계용 화면 목록 제안

현재 기능을 유지한다면 다음 화면으로 재구성할 수 있다.

1. 로그인
2. 대시보드/공지 또는 업데이트 내역
3. IP 관리
   - 전체
   - 무선
   - 유선
   - 전화기
   - 서버
   - HCI
4. 전화번호 관리
5. 스위치 포트 정보
6. 스위치 백업
7. 변경 로그
   - 전체
   - IP
   - 전화번호
8. 데이터 동기화/업데이트 상태
   - IPScan
   - 그룹웨어
   - 스위치 포트
9. 계정 관리
   - staff 전용
10. 설정
   - 테마 등 개인화 옵션

---

## 26. 핵심 기능 체크리스트

새 UI에서 누락되면 안 되는 기능은 다음과 같다.

### IP 관리

- [ ] 전체 IP 조회
- [ ] IP 분류별 조회
- [ ] 그룹/대역 필터
- [ ] 일반 검색
- [ ] 하이라이트 검색
- [ ] 퇴사 사원 조회
- [ ] 페이지당 항목 수 변경
- [ ] 컬럼 정렬
- [ ] 단건 사용자/비고 수정
- [ ] 단건 등록 해제
- [ ] 일괄 사용자/비고 수정
- [ ] 일괄 등록 해제
- [ ] Excel 다운로드

### 전화번호 관리

- [ ] 전화번호 조회
- [ ] 일반 검색
- [ ] 하이라이트 검색
- [ ] 퇴사 사원 조회
- [ ] 단건 사용자/목적/비고/IP 수정
- [ ] 단건 등록 해제
- [ ] 일괄 사용자/목적/비고/IP 수정
- [ ] 일괄 등록 해제
- [ ] IP 선택 모달
- [ ] 이미 사용 중인 IP 선택 방지
- [ ] Excel 다운로드

### 스위치 포트 정보

- [ ] 포트 정보 조회
- [ ] 스위치 IP 필터
- [ ] 검색/정렬/페이지네이션
- [ ] Excel 다운로드
- [ ] 스위치 포트 데이터 갱신 실행

### 스위치 백업

- [ ] 백업 날짜/시간 목록
- [ ] 날짜/시간별 스위치 목록
- [ ] 설정 텍스트 표시
- [ ] 전체 ZIP 다운로드
- [ ] 렉 ZIP 다운로드
- [ ] 단건 TXT 다운로드
- [ ] 설정 복사

### 로그

- [ ] 전체 로그 조회
- [ ] IP 로그 조회
- [ ] 전화번호 로그 조회
- [ ] 변경 묶음 단위 표시

### 계정 관리

- [ ] staff 사용자만 접근
- [ ] 계정 목록 조회
- [ ] 계정 생성
- [ ] 관리자 권한 설정
- [ ] 활성/비활성 설정
- [ ] 비밀번호 재설정
- [ ] 본인 계정 수정 방지

### 공통

- [ ] 로그인/로그아웃
- [ ] 현재 사용자 표시
- [ ] 테마 선택/저장
- [ ] 로딩 표시
- [ ] alert/toast 메시지
- [ ] 모달 닫기/드래그
- [ ] API 오류 처리

---

## 27. 결론

현재 웹 페이지는 단일 Django 앱 안에서 사내 IT 관리에 필요한 여러 기능을 제공한다.
핵심은 `IP_MNG`, `PHN_MNG`, 사용자/부서/회사 정보, IPScan 장비 정보, 스위치/랙/백업 정보를 조합해 테이블로 보여주고, 일부 항목은 웹에서 직접 할당/해제/수정하는 구조이다.

새로운 UI를 만들 때는 다음을 반드시 유지해야 한다.

- IP와 전화번호의 사용자 할당/해제 규칙
- 전화번호와 IP의 연동 갱신 규칙
- 사용자 선택 UX
- 전화번호용 IP 선택/중복 방지 UX
- 스위치 포트 조회/Excel 다운로드
- 스위치 백업 조회/복사/다운로드
- 로그 조회
- 관리자 계정 관리
- 외부 데이터 업데이트 버튼
- 테마/검색/페이지네이션/정렬 같은 공통 사용성 기능

이 문서를 기준으로 화면 단위와 API 단위를 분리하면, 기존 스파게티 구조에서 기능 손실 없이 새 UI/아키텍처를 설계할 수 있다.
