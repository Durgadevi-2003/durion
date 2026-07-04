document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('button[type="submit"]');
  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing';
    });
  });
});
