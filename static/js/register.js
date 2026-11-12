// =============================================
//   EpicalExam — Candidate Registration JS
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

/* ---- Step Navigation ---- */
let currentStep = 1;
const TOTAL_STEPS = 3;

function nextStep(from) {
  if (!validateStep(from)) return;
  goToStep(from + 1);
}

function prevStep(from) {
  goToStep(from - 1);
}

function goToStep(target) {
  if (target < 1 || target > TOTAL_STEPS) return;

  // Hide current
  document.getElementById(`form-step-${currentStep}`).classList.remove('active');

  // Update step dots
  for (let i = 1; i <= TOTAL_STEPS; i++) {
    const dot = document.getElementById(`step-dot-${i}`);
    dot.classList.remove('active', 'completed');
    if (i < target) dot.classList.add('completed');
    if (i === target) dot.classList.add('active');
  }

  // Update step lines
  const lines = document.querySelectorAll('.step-line');
  lines.forEach((line, idx) => {
    if (idx < target - 1) line.classList.add('filled');
    else line.classList.remove('filled');
  });

  currentStep = target;
  const nextEl = document.getElementById(`form-step-${currentStep}`);
  nextEl.classList.add('active');
  nextEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ---- Validation ---- */
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

function validateStep(step) {
  let valid = true;

  if (step === 1) {
    const first = document.getElementById('first_name').value.trim();
    const last  = document.getElementById('last_name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const dob   = document.getElementById('dob').value;
    const gender = document.querySelector('input[name="gender"]:checked');

    if (!first || first.length < 2) { showError('first_name', 'Please enter your first name.'); valid = false; } else clearError('first_name');
    if (!last || last.length < 2)   { showError('last_name', 'Please enter your last name.'); valid = false; }  else clearError('last_name');
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { showError('email', 'Enter a valid email address.'); valid = false; } else clearError('email');
    if (!phone || phone.replace(/\D/g,'').length < 10) { showError('phone', 'Enter a valid phone number.'); valid = false; } else clearError('phone');
    if (!dob)   { showError('dob', 'Please select your date of birth.'); valid = false; } else clearError('dob');
    if (!gender) { showError('gender', 'Please select your gender.'); valid = false; }
    else { const errEl = document.getElementById('err-gender'); if (errEl) { errEl.textContent = ''; errEl.classList.remove('visible'); } }
  }

  if (step === 2) {
    const roll  = document.getElementById('roll_no').value.trim();
    const dept  = document.getElementById('department').value;
    const year  = document.getElementById('year').value;
    const inst  = document.getElementById('institution').value.trim();
    const city  = document.getElementById('city').value.trim();

    if (!roll)  { showError('roll_no', 'Roll number is required.'); valid = false; } else clearError('roll_no');
    if (!dept)  { showError('department', 'Please select your department.'); valid = false; } else clearError('department');
    if (!year)  { showError('year', 'Please select your year of study.'); valid = false; } else clearError('year');
    if (!inst || inst.length < 3)  { showError('institution', 'Please enter your institution name.'); valid = false; } else clearError('institution');
    if (!city || city.length < 2)  { showError('city', 'Please enter your city.'); valid = false; } else clearError('city');
  }

  if (step === 3) {
    const pwd    = document.getElementById('password').value;
    const cpwd   = document.getElementById('confirm_password').value;
    const terms  = document.getElementById('terms').checked;
    const pwdRe  = /^(?=.*[A-Z])(?=.*\d).{8,}$/;

    if (!pwdRe.test(pwd)) { showError('password', 'Min 8 chars, 1 uppercase letter, 1 number.'); valid = false; } else clearError('password');
    if (pwd !== cpwd)     { showError('confirm_password', 'Passwords do not match.'); valid = false; } else clearError('confirm_password');
    if (!terms)           { showError('terms', 'You must agree to the Terms of Service.'); valid = false; }
    else { const errEl = document.getElementById('err-terms'); if (errEl) { errEl.textContent = ''; errEl.classList.remove('visible'); } }
  }

  return valid;
}

/* ---- Password Strength Meter ---- */
document.getElementById('password').addEventListener('input', function () {
  const val = this.value;
  const fill  = document.getElementById('strength-fill');
  const label = document.getElementById('strength-label');

  let score = 0;
  if (val.length >= 8) score++;
  if (/[A-Z]/.test(val)) score++;
  if (/[0-9]/.test(val)) score++;
  if (/[^A-Za-z0-9]/.test(val)) score++;

  const configs = [
    { pct: '0%',   color: 'transparent',            text: 'Enter a password' },
    { pct: '25%',  color: '#ef4444',                text: 'Weak' },
    { pct: '50%',  color: '#f59e0b',                text: 'Fair' },
    { pct: '75%',  color: '#06b6d4',                text: 'Good' },
    { pct: '100%', color: '#10b981',                text: 'Strong 💪' },
  ];

  const cfg = val.length === 0 ? configs[0] : configs[score];
  fill.style.width      = cfg.pct;
  fill.style.background = cfg.color;
  label.textContent     = cfg.text;
  label.style.color     = cfg.color === 'transparent' ? 'var(--text-secondary)' : cfg.color;
});

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

/* ---- Live inline validation on blur ---- */
document.querySelectorAll('input, select').forEach(el => {
  el.addEventListener('blur', () => {
    if (el.value.trim()) el.classList.add('valid');
  });
});

/* ---- Form Submit ---- */
document.getElementById('registerForm').addEventListener('submit', function (e) {
  e.preventDefault();
  if (!validateStep(3)) return;

  const btn      = document.getElementById('submitBtn');
  const textEl   = btn.querySelector('.btn-text');
  const loaderEl = btn.querySelector('.btn-loader');

  textEl.style.display   = 'none';
  loaderEl.style.display = 'flex';
  btn.disabled = true;

  // Submit the form after short delay (to show loader)
  setTimeout(() => this.submit(), 500);
});
