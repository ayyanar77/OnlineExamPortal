// =============================================
//   EpicalExam — Login Page JS
// =============================================

/* ---- Particles ---- */
(function spawnParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 30; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 4 + 2;
    p.style.cssText = `
      left: ${Math.random() * 100}%;
      width: ${size}px;
      height: ${size}px;
      animation-duration: ${Math.random() * 15 + 8}s;
      animation-delay: ${Math.random() * 10}s;
      opacity: ${Math.random() * 0.6 + 0.2};
      background: hsl(${Math.random() * 60 + 250}, 80%, 70%);
    `;
    container.appendChild(p);
  }
})();

/* ---- Toggle Password Visibility ---- */
function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId);
  const icon  = btn.querySelector('i');
  if (input.type === 'password') {
    input.type = 'text';
    icon.classList.replace('fa-eye', 'fa-eye-slash');
  } else {
    input.type = 'password';
    icon.classList.replace('fa-eye-slash', 'fa-eye');
  }
}

/* ---- Client-side Validation ---- */
function showError(fieldId, msg) {
  const errEl = document.getElementById(`err-${fieldId}`);
  const input = document.getElementById(fieldId);
  if (errEl) { errEl.textContent = msg; errEl.classList.add('visible'); }
  if (input) input.classList.add('invalid');
  return false;
}

function clearError(fieldId) {
  const errEl = document.getElementById(`err-${fieldId}`);
  const input = document.getElementById(fieldId);
  if (errEl) { errEl.textContent = ''; errEl.classList.remove('visible'); }
  if (input) { input.classList.remove('invalid'); input.classList.add('valid'); }
}

function validateLogin() {
  let valid = true;
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showError('email', 'Enter a valid email address.');
    valid = false;
  } else {
    clearError('email');
  }

  if (!password || password.length < 1) {
    showError('password', 'Please enter your password.');
    valid = false;
  } else {
    clearError('password');
  }

  return valid;
}

/* ---- Live inline validation on blur ---- */
document.querySelectorAll('input').forEach(el => {
  el.addEventListener('blur', () => {
    if (el.value.trim()) el.classList.add('valid');
  });
  el.addEventListener('input', () => {
    el.classList.remove('invalid');
    const errEl = document.getElementById(`err-${el.id}`);
    if (errEl) { errEl.textContent = ''; errEl.classList.remove('visible'); }
  });
});

/* ---- Form Submit ---- */
document.getElementById('loginForm').addEventListener('submit', function (e) {
  e.preventDefault();
  if (!validateLogin()) return;

  const btn      = document.getElementById('loginBtn');
  const textEl   = btn.querySelector('.btn-text');
  const loaderEl = btn.querySelector('.btn-loader');

  textEl.style.display   = 'none';
  loaderEl.style.display = 'flex';
  btn.disabled = true;

  // Submit the form after short delay (to show loader)
  setTimeout(() => this.submit(), 500);
});

