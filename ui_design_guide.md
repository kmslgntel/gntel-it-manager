# UI Design Guide — 사내 IT 통합 관리 시스템

이 문서는 신규 사내 IT 통합 관리 시스템의 UI/UX 구현 기준 문서입니다.

Claude Code/Hermes는 화면과 CSS를 구현할 때 이 문서를 반드시 참고합니다.

---

## 1. 디자인 목표

이 시스템은 사내 IT 관리자가 매일 사용하는 업무용 관리자 시스템입니다.

따라서 디자인 목표는 다음과 같습니다.

- 빠르게 찾을 수 있는 화면
- 오래 봐도 피로하지 않은 색상
- 데이터 테이블 중심의 명확한 구성
- IP, 전화번호, 스위치, 점검 내역을 한눈에 확인할 수 있는 가독성
- 과한 장식보다 안정감 있는 업무용 UI
- 기존 GNTEL 로고와 어울리는 파란색 계열의 정돈된 디자인

---

## 2. 브랜드 기준

### 2.1 로고

프로젝트 루트의 아래 파일을 시스템 로고로 사용합니다.

```text
./GNTEL_logo.png
```

사용 위치:

- 로그인 화면 상단 또는 좌측 영역
- 기본 레이아웃 Header 또는 Sidebar 상단
- 필요 시 Excel Export 표지/상단 영역

주의:

- 로고 비율을 깨지 않습니다.
- 로고 색상을 CSS로 임의 변경하지 않습니다.
- 로고 위에 텍스트나 아이콘을 겹치지 않습니다.
- 너무 작은 크기로 표시하지 않습니다.

권장 크기:

```css
.logo {
  width: 140px;
  height: auto;
}
```

로그인 화면에서는 더 크게 사용할 수 있습니다.

```css
.login-logo {
  width: 220px;
  height: auto;
}
```

---

## 3. 색상 시스템

GNTEL 로고는 진한 블루와 밝은 시안 계열이 중심입니다.

UI는 로고의 블루 계열을 기준으로 하되, 업무용 시스템이므로 차분하고 선명한 색상을 사용합니다.

### 3.1 핵심 색상

아래 색상만 기본 팔레트로 사용합니다.

| 용도 | 색상명 | HEX |
|---|---|---|
| Primary | GNTEL Blue | `#004A98` |
| Primary Hover | GNTEL Blue Dark | `#003A78` |
| Primary Light | GNTEL Blue Light | `#EAF3FF` |
| Accent | GNTEL Cyan | `#00B8E6` |
| Accent Light | GNTEL Cyan Light | `#E6F9FD` |
| Background | App Background | `#F5F7FA` |
| Surface | Card/Table Surface | `#FFFFFF` |
| Border | Default Border | `#D8DEE9` |
| Text Primary | Main Text | `#1F2937` |
| Text Secondary | Sub Text | `#6B7280` |
| Text Muted | Muted Text | `#9CA3AF` |
| Table Header | Table Header BG | `#EEF2F7` |
| Success | Success | `#16A34A` |
| Warning | Warning | `#F59E0B` |
| Danger | Danger/Delete | `#DC2626` |
| Disabled | Disabled | `#9CA3AF` |

### 3.2 CSS 변수

CSS에서는 아래 변수명을 기준으로 사용합니다.

```css
:root {
  --color-primary: #004A98;
  --color-primary-hover: #003A78;
  --color-primary-light: #EAF3FF;

  --color-accent: #00B8E6;
  --color-accent-light: #E6F9FD;

  --color-bg: #F5F7FA;
  --color-surface: #FFFFFF;
  --color-border: #D8DEE9;

  --color-text: #1F2937;
  --color-text-secondary: #6B7280;
  --color-text-muted: #9CA3AF;

  --color-table-header: #EEF2F7;

  --color-success: #16A34A;
  --color-warning: #F59E0B;
  --color-danger: #DC2626;
  --color-disabled: #9CA3AF;
}
```

### 3.3 색상 사용 규칙

- 주요 버튼, 선택 메뉴, 링크 강조에는 `--color-primary`를 사용합니다.
- Hover 상태에는 `--color-primary-hover`를 사용합니다.
- 정보성 강조 배경에는 `--color-primary-light` 또는 `--color-accent-light`를 사용합니다.
- 삭제, 위험 동작에는 반드시 `--color-danger`를 사용합니다.
- 성공 메시지에는 `--color-success`를 사용합니다.
- 경고 메시지에는 `--color-warning`을 사용합니다.
- 임의의 새로운 색상을 추가하지 않습니다.

---

## 4. 폰트

폰트는 Pretendard를 사용합니다.

### 4.1 기본 폰트 선언

```css
body {
  font-family: "Pretendard", "Malgun Gothic", "Apple SD Gothic Neo", Arial, sans-serif;
}
```

### 4.2 폰트 적용 방식

가능하면 로컬 static 파일 또는 CDN 중 프로젝트 상황에 맞게 적용합니다.

권장 방식 1: CDN

```html
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css" />
```

권장 방식 2: static 파일

```text
static/fonts/pretendard/
```

사내망에서 외부 CDN 접근이 제한될 수 있으므로, 배포 환경에서는 static 파일 방식이 더 안전합니다.

### 4.3 폰트 크기 기준

| 요소 | 크기 | 굵기 |
|---|---:|---:|
| Page Title | 24px | 700 |
| Section Title | 18px | 700 |
| Card Title | 16px | 600 |
| Body Text | 14px | 400 |
| Table Text | 13px | 400 |
| Table Header | 13px | 600 |
| Button | 14px | 600 |
| Help Text | 12px | 400 |

---

## 5. 레이아웃 기준

레이아웃은 복잡하게 만들지 않고, 전형적인 관리자 시스템 구조를 사용합니다.

### 5.1 기본 구조

```text
+------------------------------------------------------+
| Header                                               |
| Logo / System Name                 User / Logout     |
+---------------+--------------------------------------+
| Sidebar       | Main Content                         |
|               |                                      |
| Dashboard     | Page Title                           |
| IP 관리       | Search / Filter / Action Buttons     |
| 전화번호      | Table / Form / Detail                |
| 스위치        | Pagination                           |
| 정기점검      |                                      |
| 계정작업      |                                      |
| 로그          |                                      |
+---------------+--------------------------------------+
```

### 5.2 Header

Header에는 다음 요소를 둡니다.

- 좌측: GNTEL 로고 또는 시스템명
- 우측: 로그인 사용자명, 로그아웃 버튼

권장 높이:

```css
.header {
  height: 56px;
}
```

### 5.3 Sidebar

Sidebar에는 주요 메뉴를 둡니다.

메뉴 구성:

- Dashboard
- IP 관리
- 전화번호 관리
- 스위치 관리
- 스위치 백업
- 정기점검
- 계정 작업
- 변경 로그
- 관리자 메뉴

권장 너비:

```css
.sidebar {
  width: 240px;
}
```

Sidebar 색상:

- 배경: `#FFFFFF` 또는 `#F8FAFC`
- 선택 메뉴: `--color-primary-light`
- 선택 메뉴 텍스트: `--color-primary`
- 좌측 선택 바: `--color-primary`

주의:

- Sidebar 전체를 너무 어두운 색으로 만들지 않습니다.
- 로고의 블루를 살리기 위해 밝은 관리자형 사이드바를 기본으로 합니다.

### 5.4 Main Content

Main Content는 카드와 테이블 중심으로 구성합니다.

권장 여백:

```css
.main-content {
  padding: 24px;
}
```

Page Title 아래에는 설명 문구나 현재 필터 상태를 표시할 수 있습니다.

---

## 6. 화면별 UI 기준

### 6.1 로그인 화면

로그인 화면은 단순하고 명확하게 구성합니다.

구성:

- 중앙 또는 좌우 분할 레이아웃
- GNTEL 로고
- 시스템명: 사내 IT 통합 관리 시스템
- Username
- Password
- Sign In 버튼
- 오류 메시지

권장:

- 배경은 `--color-bg`
- 로그인 박스는 흰색 카드
- Primary 버튼은 GNTEL Blue

### 6.2 Dashboard

Dashboard에는 주요 현황 카드와 빠른 이동 링크를 둡니다.

예:

- IP 총 수
- 사용 중 IP 수
- 전화번호 수
- 스위치 수
- 이번 달 정기점검 상태
- 최근 계정 작업
- 최근 변경 로그

### 6.3 목록 화면

IP, 전화번호, 스위치, 계정 작업, 변경 로그 화면은 공통 목록 구조를 사용합니다.

구성:

1. Page Title
2. 검색/필터 영역
3. 주요 버튼 영역
4. 데이터 테이블
5. 페이지네이션

### 6.4 등록/수정 화면

등록/수정 화면은 일반 Django Form 페이지로 구현합니다.

구성:

- Page Title
- 입력 Form Card
- 필드 Label
- 입력 요소
- 필드별 에러 메시지
- 저장 버튼
- 취소 버튼

### 6.5 상세 화면

상세 화면은 요약 카드와 관련 테이블을 함께 사용합니다.

예:

- IP 상세
  - IP 정보 카드
  - 사용자 정보 카드
  - 장비/IPScan 정보 카드
  - 변경 로그 테이블

---

## 7. 테이블 디자인 기준

업무 시스템의 핵심은 테이블입니다.

### 7.1 기본 테이블

```css
.table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  font-size: 13px;
}

.table th {
  background: var(--color-table-header);
  color: var(--color-text);
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
}

.table td {
  border-bottom: 1px solid var(--color-border);
}

.table tr:hover {
  background: var(--color-primary-light);
}
```

### 7.2 테이블 규칙

- 기본 행 수는 100개를 권장합니다.
- 데이터가 많을 경우 페이지네이션을 사용합니다.
- 빈 값은 빈칸 대신 `-`로 표시합니다.
- 긴 값은 줄바꿈 또는 tooltip/title 속성을 사용합니다.
- 테이블이 화면보다 넓으면 가로 스크롤을 허용합니다.
- 삭제 버튼은 텍스트 또는 간단한 `삭제` 버튼으로 표시합니다.
- UI에 이모지를 사용하지 않습니다.

---

## 8. 버튼 디자인 기준

### 8.1 버튼 종류

| 종류 | 용도 | 색상 |
|---|---|---|
| Primary | 저장, 등록, 주요 실행 | `--color-primary` |
| Secondary | 취소, 뒤로, 보조 동작 | 흰색 + border |
| Success | 완료, export 성공 | `--color-success` |
| Warning | 재확인 필요 | `--color-warning` |
| Danger | 삭제, 위험 명령 | `--color-danger` |

### 8.2 버튼 텍스트

좋은 예:

- 저장
- 등록
- 수정
- 삭제
- 검색
- 초기화
- Excel 다운로드
- 로그아웃
- 명령 실행

나쁜 예:

- 🚀 실행
- 🔥 삭제
- ✨ 저장
- Go!
- Click Here

---

## 9. Form 디자인 기준

- Label은 항상 표시합니다.
- 필수값은 `필수` 텍스트 또는 `*`로 표시합니다.
- 에러 메시지는 해당 필드 바로 아래 표시합니다.
- placeholder만으로 필드 의미를 설명하지 않습니다.
- 날짜 입력은 가능한 HTML date input을 사용합니다.
- 긴 설명은 textarea를 사용합니다.
- 저장/취소 버튼은 Form 하단에 고정 배치합니다.

---

## 10. 반응형 기준

주 사용 환경은 사내 PC 브라우저입니다.

기준:

- 1280px 이상 화면에서 최적화
- 모바일 전용 UI는 필수 아님
- 화면 폭이 좁아지면 테이블은 가로 스크롤 허용
- Sidebar는 작은 화면에서 접히는 구조를 선택적으로 구현 가능

---

## 11. Anti-pattern 방지 규칙

아래 규칙은 반드시 지킵니다.

### 11.1 NO GRADIENTS

Gradient를 사용하지 않습니다.

금지:

```css
background: linear-gradient(...);
background-image: radial-gradient(...);
```

허용:

```css
background: var(--color-primary);
background: var(--color-bg);
```

### 11.2 NO CUSTOM COLORS

이 문서의 색상 팔레트에 없는 임의 색상을 새로 만들지 않습니다.

금지:

```css
color: #123456;
background: #ff00aa;
```

허용:

```css
color: var(--color-text);
background: var(--color-primary);
```

새 색상이 꼭 필요하면 먼저 이 문서의 팔레트에 추가한 뒤 사용합니다.

### 11.3 NO EXCESSIVE ANIMATIONS

과한 애니메이션을 사용하지 않습니다.

금지:

- 흔들리는 버튼
- 반복되는 pulse 효과
- 자동으로 움직이는 배경
- 과한 hover transform
- 긴 transition

허용:

```css
transition: background-color 0.15s ease, border-color 0.15s ease;
```

### 11.4 NO EMOJIS IN UI

UI 텍스트, 메뉴명, 버튼명, 제목, 알림 메시지에 이모지를 사용하지 않습니다.

금지:

- 📌 Dashboard
- 🔥 삭제
- ✅ 저장 완료
- 🚀 실행

허용:

- Dashboard
- 삭제
- 저장 완료
- 실행

### 11.5 NO DECORATIVE UI OVER FUNCTION

기능보다 장식이 우선되는 UI를 만들지 않습니다.

금지:

- 지나치게 큰 카드
- 의미 없는 아이콘 남발
- 데이터보다 장식이 더 많은 화면
- 업무 테이블을 보기 어렵게 만드는 디자인

---

## 12. CSS 파일 구조

권장 구조:

```text
static/
  css/
    base.css       # reset, variables, typography
    layout.css     # header, sidebar, main layout
    table.css      # table, pagination
    form.css       # form, input, validation
    button.css     # buttons
    page.css       # page-specific minor styles
  js/
    common.js
```

복잡한 프론트엔드 프레임워크는 사용하지 않습니다.

---

## 13. Template 구조

권장 구조:

```text
templates/
  base.html
  dashboard.html
  registration/
    login.html
  assets/
    ip_list.html
    ip_form.html
    ip_detail.html
    phone_list.html
    phone_form.html
    phone_detail.html
  switches/
    switch_list.html
    switch_detail.html
    switch_ports.html
    switch_backups.html
    switch_command.html
  inspection/
    inspection_list.html
    inspection_form.html
    inspection_detail.html
  accounts_work/
    accountwork_list.html
    accountwork_form.html
  core/
    auditlog_list.html
```

---

## 14. Excel 양식 기준

정기점검 Excel Export는 프로젝트 루트에 있는 아래 파일을 기준 양식으로 사용합니다.

```text
./●월간 서버 점검리스트_2026년_4월.xlsx
```

이 파일은 실제 제출용 월간 서버 점검리스트 양식입니다.

구현 방침:

- `openpyxl`로 이 파일을 템플릿처럼 읽어 사용합니다.
- 원본 파일은 수정하지 않습니다.
- Export 시 원본을 복사한 뒤 해당 월의 점검 데이터를 채웁니다.
- Export 결과 파일명 예:

```text
월간_서버_점검리스트_2026년_05월.xlsx
```

- 셀 위치를 정확히 알 수 없는 경우 먼저 양식의 시트명, 병합 셀, 주요 라벨 셀을 분석합니다.
- 분석 후 코드에 셀 매핑 테이블을 명시합니다.
- 계정 작업 내역이 별도 시트 또는 별도 영역에 필요하면 같은 workbook 안에 추가 시트로 생성합니다.
- 양식 파일이 없는 환경에서도 명확한 오류 메시지를 표시하거나 기본 양식 fallback을 제공합니다.

---

## 15. Claude Code 구현 지시 요약

Claude Code는 UI 구현 시 아래를 따른다.

1. 사용자가 HTML/CSS를 따로 제공한다고 가정하지 않는다.
2. 이 `ui_design_guide.md` 기준으로 직접 깔끔한 관리자형 UI를 구현한다.
3. GNTEL 로고와 어울리는 블루/시안 계열 팔레트를 사용한다.
4. Pretendard 폰트를 사용한다.
5. 테이블 중심의 업무용 UI로 구현한다.
6. Gradient를 사용하지 않는다.
7. 임의 색상을 추가하지 않는다.
8. 과한 애니메이션을 사용하지 않는다.
9. UI에 이모지를 사용하지 않는다.
10. 기능 없는 더미 화면으로 끝내지 않는다.
