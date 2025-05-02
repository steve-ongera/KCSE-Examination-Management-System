document.getElementById('togglePassword').addEventListener('click', function () {
  const passwordField = document.getElementById('password');
  const icon = this.querySelector('i'); // target the <i> inside the button

  if (passwordField.type === 'password') {
    passwordField.type = 'text';
    icon.classList.remove('bi-eye-slash');
    icon.classList.add('bi-eye');
  } else {
    passwordField.type = 'password';
    icon.classList.remove('bi-eye');
    icon.classList.add('bi-eye-slash');
  }
});




  
  
  // Toggle Password visibility for "Confirm Password" field
  document.getElementById('togglePassword2').addEventListener('click', function () {
    const confirmPasswordField = document.getElementById('password2');
    const icon = document.getElementById('togglePassword2');
  
    if (confirmPasswordField.type === 'password') {
      confirmPasswordField.type = 'text';
      icon.classList.remove('bi-eye-slash');
      icon.classList.add('bi-eye');
    } else {
      confirmPasswordField.type = 'password';
      icon.classList.remove('bi-eye');
      icon.classList.add('bi-eye-slash');
    }
  });
  
  