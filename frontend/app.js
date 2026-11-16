// API Base URL (relative path works when served from FastAPI)
const API_BASE = '/gym';

// Helper: Show Toast Notification
function showToast(message, isError = false) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.style.borderLeftColor = isError ? '#991B1B' : 'var(--swiss-tan)';
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3500);
}

// Set default dates for date inputs
function setDefaultDates() {
  const today = new Date().toISOString().split('T')[0];
  const nextMonth = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

  ['mem-join', 'mem-start', 'pay-date', 'att-date'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = today;
  });

  ['mem-end', 'renew-date'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = nextMonth;
  });
}

// 1. Fetch & Display Overview KPI Metrics
async function loadMetrics() {
  try {
    const [membersRes, trainersRes, expiringRes, revenueRes] = await Promise.all([
      fetch(`${API_BASE}/all`),
      fetch(`${API_BASE}/trainers`),
      fetch(`${API_BASE}/memberships/expiring`),
      fetch(`${API_BASE}/payments/revenue`)
    ]);

    if (membersRes.ok) {
      const members = await membersRes.json();
      document.getElementById('kpi-members').textContent = members.length;
    }

    if (trainersRes.ok) {
      const trainers = await trainersRes.json();
      document.getElementById('kpi-trainers').textContent = trainers.length;
    }

    if (expiringRes.ok) {
      const expiring = await expiringRes.json();
      document.getElementById('kpi-expiring').textContent = expiring.length;
    }

    if (revenueRes.ok) {
      const data = await revenueRes.json();
      const rev = data.total_revenue || 0;
      document.getElementById('kpi-revenue').textContent = `$${rev.toLocaleString()}`;
      document.getElementById('revenue-display').textContent = `$${rev.toLocaleString()}`;
    }
  } catch (err) {
    console.warn('API fetch warning:', err);
  }
}

// 2. Fetch & Render Members Table
async function loadMembers() {
  const tbody = document.getElementById('members-tbody');
  try {
    const res = await fetch(`${API_BASE}/all`);
    if (!res.ok) throw new Error('Failed to fetch members');
    const members = await res.json();

    if (members.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding: 2rem;">No member records found.</td></tr>';
      return;
    }

    tbody.innerHTML = members.map(m => `
      <tr>
        <td><strong>#${m.uid}</strong></td>
        <td>${escapeHtml(m.name)}</td>
        <td>$${m.fees.toLocaleString()}</td>
        <td>${m.tid ? `Trainer #${m.tid}` : '<span style="color:var(--swiss-grey);">Unassigned</span>'}</td>
        <td>${m.joining_date}</td>
        <td>
          <button class="button button--danger button--small" onclick="deleteMember(${m.uid})" aria-label="Delete member ${escapeHtml(m.name)}">
            Delete
          </button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:#991B1B;">Error loading members: ${err.message}</td></tr>`;
  }
}

// 3. Fetch & Render Trainers Table
async function loadTrainers() {
  const tbody = document.getElementById('trainers-tbody');
  try {
    const res = await fetch(`${API_BASE}/trainers`);
    if (!res.ok) throw new Error('Failed to fetch trainers');
    const trainers = await res.json();

    if (trainers.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 2rem;">No trainers registered.</td></tr>';
      return;
    }

    tbody.innerHTML = trainers.map(t => `
      <tr>
        <td><strong>#${t.tid}</strong></td>
        <td>${escapeHtml(t.name)}</td>
        <td>${escapeHtml(t.email)}</td>
        <td>$${t.salary.toLocaleString()}</td>
        <td>
          <button class="button button--outline button--small" onclick="viewTrainees(${t.tid}, '${escapeHtml(t.name)}')">
            View Trainees
          </button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:#991B1B;">Error loading trainers: ${err.message}</td></tr>`;
  }
}

// View Trainees assigned to Trainer
window.viewTrainees = async function(tid, trainerName) {
  const modal = document.getElementById('modal-trainees');
  const title = document.getElementById('modal-trainees-title');
  const container = document.getElementById('trainees-list-container');

  title.textContent = `Trainees Assigned to ${trainerName} (TID #${tid})`;
  container.innerHTML = '<p>Loading assigned trainees...</p>';
  modal.classList.add('open');

  try {
    const res = await fetch(`${API_BASE}/trainers/${tid}/members`);
    if (!res.ok) throw new Error('Could not fetch trainer members');
    const trainees = await res.json();

    if (trainees.length === 0) {
      container.innerHTML = '<p style="padding: 1.5rem 0;">No active members assigned to this trainer.</p>';
      return;
    }

    container.innerHTML = `
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>UID</th>
              <th>Member Name</th>
              <th>Monthly Fee</th>
              <th>Joined</th>
            </tr>
          </thead>
          <tbody>
            ${trainees.map(m => `
              <tr>
                <td>#${m.uid}</td>
                <td><strong>${escapeHtml(m.name)}</strong></td>
                <td>$${m.fees}</td>
                <td>${m.joining_date}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    `;
  } catch (err) {
    container.innerHTML = `<p style="color:#991B1B;">Error: ${err.message}</p>`;
  }
};

// Delete Member
window.deleteMember = async function(uid) {
  if (!confirm(`Are you sure you want to delete member #${uid}?`)) return;

  try {
    const res = await fetch(`${API_BASE}/member/${uid}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Deletion failed');
    showToast(`Member #${uid} removed.`);
    loadMembers();
    loadMetrics();
  } catch (err) {
    showToast(err.message, true);
  }
};

// Form: Register Member
document.getElementById('form-create-member').addEventListener('submit', async (e) => {
  e.preventDefault();
  const tidVal = document.getElementById('mem-tid').value;
  const payload = {
    name: document.getElementById('mem-name').value,
    fees: parseInt(document.getElementById('mem-fees').value, 10),
    tid: tidVal ? parseInt(tidVal, 10) : null,
    joining_date: document.getElementById('mem-join').value
  };

  try {
    const res = await fetch(`${API_BASE}/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Registration failed');
    const created = await res.json();
    showToast(`Member created: #${created.uid} ${created.name}`);
    document.getElementById('modal-member').classList.remove('open');
    e.target.reset();
    setDefaultDates();
    loadMembers();
    loadMetrics();
  } catch (err) {
    showToast(err.message, true);
  }
});

// Form: Create Trainer
document.getElementById('form-create-trainer').addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    name: document.getElementById('tr-name').value,
    email: document.getElementById('tr-email').value,
    salary: parseInt(document.getElementById('tr-salary').value, 10)
  };

  try {
    const res = await fetch(`${API_BASE}/trainers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Trainer addition failed');
    const created = await res.json();
    showToast(`Trainer added: #${created.tid} ${created.name}`);
    document.getElementById('modal-trainer').classList.remove('open');
    e.target.reset();
    loadTrainers();
    loadMetrics();
  } catch (err) {
    showToast(err.message, true);
  }
});

// Form: Issue Membership
document.getElementById('form-new-membership').addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    member_id: parseInt(document.getElementById('mem-member-id').value, 10),
    start_date: document.getElementById('mem-start').value,
    end_date: document.getElementById('mem-end').value,
    status: 'Active'
  };

  try {
    const res = await fetch(`${API_BASE}/memberships`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Membership assignment failed');
    const created = await res.json();
    showToast(`Membership #${created.membership_id} issued.`);
    e.target.reset();
    setDefaultDates();
    loadMetrics();
  } catch (err) {
    showToast(err.message, true);
  }
});

// Form: Renew Membership
document.getElementById('form-renew-membership').addEventListener('submit', async (e) => {
  e.preventDefault();
  const membershipId = parseInt(document.getElementById('renew-id').value, 10);
  const payload = {
    new_end_date: document.getElementById('renew-date').value,
    status: 'Active'
  };

  try {
    const res = await fetch(`${API_BASE}/memberships/${membershipId}/renew`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Renewal failed');
    showToast(`Membership #${membershipId} successfully renewed.`);
    e.target.reset();
    setDefaultDates();
    loadMetrics();
  } catch (err) {
    showToast(err.message, true);
  }
});

// Form: Log Payment
document.getElementById('form-create-payment').addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    member_id: parseInt(document.getElementById('pay-member-id').value, 10),
    amount: parseInt(document.getElementById('pay-amount').value, 10),
    date: document.getElementById('pay-date').value,
    status: document.getElementById('pay-status').value
  };

  try {
    const res = await fetch(`${API_BASE}/payments/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Payment entry failed');
    showToast('Payment recorded successfully.');
    e.target.reset();
    setDefaultDates();
    loadMetrics();
  } catch (err) {
    showToast(err.message, true);
  }
});

// Form: Attendance Check-in
document.getElementById('form-checkin').addEventListener('submit', async (e) => {
  e.preventDefault();
  const memberId = document.getElementById('att-member-id').value;
  const dateVal = document.getElementById('att-date').value;

  try {
    const res = await fetch(`${API_BASE}/attendance/check-in?member_id=${memberId}&date=${dateVal}&status=Present`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error('Check-in failed');
    showToast(`Member #${memberId} marked Present.`);
    e.target.reset();
    setDefaultDates();
  } catch (err) {
    showToast(err.message, true);
  }
});

// Form: Workout Schedule Assignment
document.getElementById('form-schedule').addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    member_id: parseInt(document.getElementById('sch-member-id').value, 10),
    trainer_id: parseInt(document.getElementById('sch-trainer-id').value, 10),
    workout_details: document.getElementById('sch-details').value
  };

  try {
    const res = await fetch(`${API_BASE}/schedules`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Schedule assignment failed');
    showToast('Workout schedule saved.');
    e.target.reset();
  } catch (err) {
    showToast(err.message, true);
  }
});

// Refresh Revenue Button
document.getElementById('btn-refresh-revenue').addEventListener('click', loadMetrics);

// Modal Open / Close Handlers
document.getElementById('btn-open-member-modal').addEventListener('click', () => {
  document.getElementById('modal-member').classList.add('open');
});
document.getElementById('btn-close-member-modal').addEventListener('click', () => {
  document.getElementById('modal-member').classList.remove('open');
});

document.getElementById('btn-open-trainer-modal').addEventListener('click', () => {
  document.getElementById('modal-trainer').classList.add('open');
});
document.getElementById('btn-close-trainer-modal').addEventListener('click', () => {
  document.getElementById('modal-trainer').classList.remove('open');
});

document.getElementById('btn-close-trainees-modal').addEventListener('click', () => {
  document.getElementById('modal-trainees').classList.remove('open');
});

// Close modal on background click
window.addEventListener('click', (e) => {
  ['modal-member', 'modal-trainer', 'modal-trainees'].forEach(id => {
    const modal = document.getElementById(id);
    if (e.target === modal) modal.classList.remove('open');
  });
});

// Navigation Highlight on Click & Scroll
document.querySelectorAll('.nav__link').forEach(link => {
  link.addEventListener('click', (e) => {
    document.querySelectorAll('.nav__link').forEach(l => l.classList.remove('active'));
    link.classList.add('active');
  });
});

// Simple HTML escaping helper
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Initial Boot
document.addEventListener('DOMContentLoaded', () => {
  setDefaultDates();
  loadMetrics();
  loadMembers();
  loadTrainers();
});
