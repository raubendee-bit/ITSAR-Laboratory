const API = {
  students:    'http://localhost:8001',
  courses:     'http://localhost:8002',
  enrollments: 'http://localhost:8003'
};

// ── Toast ──────────────────────────────────────────────
function toast(msg, type = 'info') {
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.textContent = msg;
  document.getElementById('toasts').appendChild(el);
  setTimeout(() => el.remove(), 3200);
}

// ── Health Check ───────────────────────────────────────
async function checkHealth() {
  const checks = [
    { id: 'hp-8001', url: `${API.students}/students` },
    { id: 'hp-8002', url: `${API.courses}/courses` },
    { id: 'hp-8003', url: `${API.enrollments}/enrollments` },
  ];
  for (const c of checks) {
    const el = document.getElementById(c.id);
    try {
      const r = await fetch(c.url, { signal: AbortSignal.timeout(2000) });
      el.className = `health-pill ${r.ok ? 'up' : 'down'}`;
    } catch {
      el.className = 'health-pill down';
    }
  }
}

// ── Students ──────────────────────────────────────────
async function loadStudents() {
  try {
    const data = await fetch(`${API.students}/students`).then(r => r.json());
    document.getElementById('cnt-students').textContent = data.length;

    const sel = document.getElementById('e-student');
    const prev = sel.value;
    sel.innerHTML = '<option value="">— select student —</option>' +
      data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
    sel.value = prev;

    const list = document.getElementById('list-students');
    if (!data.length) {
      list.innerHTML = `<div class="empty"><div class="empty-icon">👤</div>No students yet</div>`;
      return;
    }
    list.innerHTML = data.map(s => `
      <div class="list-item">
        <span class="item-id">#${s.id}</span>
        <div class="item-main">
          <div class="item-name">${s.name}</div>
          <div class="item-sub">${s.email}</div>
        </div>
        <span class="item-tag tag-blue">student</span>
        <button class="del-btn" onclick="deleteStudent(${s.id})">✕</button>
      </div>`).join('');
  } catch {}
}

async function addStudent() {
  const name  = document.getElementById('s-name').value.trim();
  const email = document.getElementById('s-email').value.trim();
  if (!name || !email) { toast('Name and email are required', 'error'); return; }
  try {
    const res  = await fetch(`${API.students}/students`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email })
    });
    const data = await res.json();
    if (!res.ok) { toast(data.error || 'Failed', 'error'); return; }
    toast(`"${data.name}" added!`, 'success');
    document.getElementById('s-name').value = '';
    document.getElementById('s-email').value = '';
    loadStudents();
  } catch { toast('Student service offline (port 8001)', 'error'); }
}

async function deleteStudent(id) {
  try {
    await fetch(`${API.students}/students/${id}`, { method: 'DELETE' });
    toast('Student removed', 'info');
    loadStudents();
  } catch { toast('Delete failed', 'error'); }
}

// ── Courses ───────────────────────────────────────────
async function loadCourses() {
  try {
    const data = await fetch(`${API.courses}/courses`).then(r => r.json());
    document.getElementById('cnt-courses').textContent = data.length;

    const sel = document.getElementById('e-course');
    const prev = sel.value;
    sel.innerHTML = '<option value="">— select course —</option>' +
      data.map(c => `<option value="${c.id}">${c.title}</option>`).join('');
    sel.value = prev;

    const list = document.getElementById('list-courses');
    if (!data.length) {
      list.innerHTML = `<div class="empty"><div class="empty-icon">📚</div>No courses yet</div>`;
      return;
    }
    list.innerHTML = data.map(c => `
      <div class="list-item">
        <span class="item-id">#${c.id}</span>
        <div class="item-main">
          <div class="item-name">${c.title}</div>
          <div class="item-sub">${c.credits} credit${c.credits !== 1 ? 's' : ''}</div>
        </div>
        <span class="item-tag tag-amber">${c.credits} cr</span>
        <button class="del-btn" onclick="deleteCourse(${c.id})">✕</button>
      </div>`).join('');
  } catch {}
}

async function addCourse() {
  const title   = document.getElementById('c-title').value.trim();
  const credits = document.getElementById('c-credits').value.trim();
  if (!title || !credits) { toast('Title and credits are required', 'error'); return; }
  try {
    const res  = await fetch(`${API.courses}/courses`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, credits: parseInt(credits) })
    });
    const data = await res.json();
    if (!res.ok) { toast(data.error || 'Failed', 'error'); return; }
    toast(`"${data.title}" added!`, 'success');
    document.getElementById('c-title').value = '';
    document.getElementById('c-credits').value = '';
    loadCourses();
  } catch { toast('Course service offline (port 8002)', 'error'); }
}

async function deleteCourse(id) {
  try {
    await fetch(`${API.courses}/courses/${id}`, { method: 'DELETE' });
    toast('Course removed', 'info');
    loadCourses();
  } catch { toast('Delete failed', 'error'); }
}

// ── Enrollments ───────────────────────────────────────
async function loadEnrollments() {
  try {
    const data = await fetch(`${API.enrollments}/enrollments`).then(r => r.json());
    document.getElementById('cnt-enrollments').textContent = data.length;

    const list = document.getElementById('list-enrollments');
    if (!data.length) {
      list.innerHTML = `<div class="empty"><div class="empty-icon">📋</div>No enrollments yet</div>`;
      return;
    }
    list.innerHTML = data.map(e => `
      <div class="list-item">
        <span class="item-id">#${e.id}</span>
        <div class="item-main">
          <div class="item-name">${e.student.name}</div>
          <div class="item-sub">${e.course.title}</div>
        </div>
        <span class="item-tag tag-green">${e.course.credits} cr</span>
      </div>`).join('');
  } catch {}
}

async function addEnrollment() {
  const student_id = document.getElementById('e-student').value;
  const course_id  = document.getElementById('e-course').value;
  if (!student_id || !course_id) { toast('Select a student and a course', 'error'); return; }
  try {
    const res  = await fetch(`${API.enrollments}/enrollments`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: parseInt(student_id), course_id: parseInt(course_id) })
    });
    const data = await res.json();
    if (!res.ok) { toast(data.error || 'Enrollment failed', 'error'); return; }
    toast('Enrolled successfully!', 'success');
    loadEnrollments();
  } catch { toast('Enrollment service offline (port 8003)', 'error'); }
}

// ── Init ──────────────────────────────────────────────
checkHealth();
setInterval(checkHealth, 5000);
loadStudents();
loadCourses();
loadEnrollments();
