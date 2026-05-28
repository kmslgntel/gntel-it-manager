/* common.js — 공통 JS */

document.addEventListener('DOMContentLoaded', function () {

  // Sidebar: 현재 URL과 일치하는 메뉴에 active 클래스 적용
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-item').forEach(function (item) {
    const href = item.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      item.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      item.classList.add('active');
    }
  });

  // 삭제 확인 다이얼로그
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      const msg = el.getAttribute('data-confirm') || '정말 삭제하시겠습니까?';
      if (!window.confirm(msg)) {
        e.preventDefault();
      }
    });
  });

  // 메시지 자동 닫기 (5초)
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      el.style.transition = 'opacity 0.3s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 300);
    });
  }, 5000);

});
