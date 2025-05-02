document.addEventListener('DOMContentLoaded', function () {
    const toggleIcons = document.querySelectorAll('.toggle-password');
  
    toggleIcons.forEach(function (icon) {
      icon.addEventListener('click', function () {
        const targetId = this.getAttribute('data-target');
        const passwordField = document.getElementById(targetId);
  
        if (!passwordField) return;
  
        if (passwordField.type === 'password') {
          passwordField.type = 'text';
          this.classList.remove('bi-eye-slash');
          this.classList.add('bi-eye');
        } else {
          passwordField.type = 'password';
          this.classList.remove('bi-eye');
          this.classList.add('bi-eye-slash');
        }
      });
    });
  });
  