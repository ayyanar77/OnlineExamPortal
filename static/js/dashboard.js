// =============================================
//   EpicalExam — Dashboard JS
// =============================================

/* ---- Sidebar Toggle (Mobile) ---- */
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

/* ---- Section Navigation ---- */
function showSection(sectionName) {
  // Hide all sections
  document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));

  // Show target section
  const target = document.getElementById(`section-${sectionName}`);
  if (target) target.classList.add('active');

  // Update nav items
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.remove('active');
    if (item.dataset.section === sectionName) item.classList.add('active');
  });

  // Close sidebar on mobile
  document.getElementById('sidebar').classList.remove('open');
}

/* ---- Nav Item Clicks ---- */
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', function (e) {
    e.preventDefault();
    const section = this.dataset.section;
    if (section) showSection(section);
  });
});

/* ---- Animated Stat Counters ---- */
function animateCounters() {
  document.querySelectorAll('.stat-value[data-target]').forEach(el => {
    const target = parseInt(el.dataset.target) || 0;
    if (target === 0) { el.textContent = '0'; return; }

    let current = 0;
    const increment = Math.max(1, Math.floor(target / 30));
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        el.textContent = target;
        clearInterval(timer);
      } else {
        el.textContent = current;
      }
    }, 30);
  });
}

// Check hash on load (e.g. #exams or #results)
window.addEventListener('DOMContentLoaded', () => {
  const hash = window.location.hash.replace('#', '');
  if (hash && document.getElementById(`section-${hash}`)) {
    showSection(hash);
  }
});

// Run counter animation on load
animateCounters();

