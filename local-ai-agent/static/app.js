const apiHeaders = {'Content-Type': 'application/json'};
let authHeader = localStorage.getItem('authHeader');

function getHeaders() {
  const headers = { ...apiHeaders };
  if (authHeader) {
    headers.Authorization = authHeader;
  }
  return headers;
}

function updateAuthStatus() {
  const status = document.getElementById('authStatus');
  status.textContent = authHeader ? 'Logged in' : 'Not logged in';
}

function login() {
  const username = document.getElementById('usernameInput').value;
  const password = document.getElementById('passwordInput').value;
  authHeader = 'Basic ' + btoa(`${username}:${password}`);
  localStorage.setItem('authHeader', authHeader);
  updateAuthStatus();
}

function logout() {
  authHeader = null;
  localStorage.removeItem('authHeader');
  updateAuthStatus();
}

async function runShellCommand() {
  const command = document.getElementById('cmdInput').value;
  const description = document.getElementById('cmdDescription').value;
  const response = await fetch('/run', {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ command, description }),
  });
  const data = await response.json();
  document.getElementById('cmdResult').textContent = JSON.stringify(data, null, 2);
}

async function requestAutomation() {
  const action = document.getElementById('automationAction').value;
  const x = parseInt(document.getElementById('automationX').value) || null;
  const y = parseInt(document.getElementById('automationY').value) || null;
  const text = document.getElementById('automationText').value || null;
  const key = document.getElementById('automationKey').value || null;
  const keys = document.getElementById('automationKeys').value
    .split(',')
    .map(k => k.trim())
    .filter(Boolean);
  const button = document.getElementById('automationButton').value;
  const interval = parseFloat(document.getElementById('automationInterval').value);
  const duration = parseFloat(document.getElementById('automationDuration').value);
  const seconds = parseFloat(document.getElementById('automationSeconds').value);

  const payload = { action, x, y, text, key, keys: keys.length ? keys : null, button, interval, duration, seconds };
  const response = await fetch('/automation/request', {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  document.getElementById('automationResult').textContent = JSON.stringify(data, null, 2);
  loadPendingAutomation();
}

async function toggleSandbox(enable) {
  const path = enable ? '/sandbox/enable' : '/sandbox/disable';
  const response = await fetch(path, {
    method: 'POST',
    headers: getHeaders(),
  });
  const data = await response.json();
  alert(JSON.stringify(data, null, 2));
  checkSandboxStatus();
}

async function checkSandboxStatus() {
  const response = await fetch('/sandbox/status', {
    headers: getHeaders(),
  });
  const data = await response.json();
  document.getElementById('sandboxStatus').textContent = JSON.stringify(data, null, 2);
}

async function loadPendingAutomation() {
  const response = await fetch('/automation/pending', {
    headers: getHeaders(),
  });
  const data = await response.json();
  const list = data.requests || [];
  const container = document.getElementById('pendingList');
  if (!list.length) {
    container.innerHTML = '<p>No pending automation requests.</p>';
    return;
  }
  container.innerHTML = list.map(item => `
    <div style="margin-bottom: 12px; padding: 10px; background: #222; border-radius: 8px;">
      <strong>${item.action.action}</strong> <span class="badge">${item.status}</span><br />
      <pre style="white-space: pre-wrap;">${JSON.stringify(item.action, null, 2)}</pre>
      <button onclick="confirmAutomation('${item.id}')">Confirm</button>
      <button onclick="cancelAutomation('${item.id}')">Cancel</button>
    </div>
  `).join('');
}

async function confirmAutomation(requestId) {
  const response = await fetch('/automation/confirm', {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ request_id: requestId }),
  });
  const data = await response.json();
  alert(JSON.stringify(data, null, 2));
  loadPendingAutomation();
}

async function cancelAutomation(requestId) {
  const response = await fetch('/automation/cancel', {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ request_id: requestId }),
  });
  const data = await response.json();
  alert(JSON.stringify(data, null, 2));
  loadPendingAutomation();
}

async function loadVMs() {
  const response = await fetch('/vm/list', {
    headers: getHeaders(),
  });
  const data = await response.json();
  const container = document.getElementById('vmList');
  if (data.error) {
    container.innerHTML = `<p>${data.error}</p>`;
    return;
  }
  if (!data.vms || !data.vms.length) {
    container.innerHTML = '<p>No VirtualBox VMs found.</p>';
    return;
  }
  container.innerHTML = data.vms.map(name => `
    <div style="margin-bottom: 10px; padding: 10px; background: #222; border-radius: 8px;">
      <strong>${name}</strong>
      <div class="row">
        <button onclick="startVM('${name}')">Start</button>
        <button onclick="stopVM('${name}')">Stop</button>
      </div>
    </div>
  `).join('');
}

async function startVM(name) {
  const response = await fetch('/vm/start', {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ name }),
  });
  const data = await response.json();
  alert(JSON.stringify(data, null, 2));
}

async function stopVM(name) {
  const response = await fetch('/vm/stop', {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ name }),
  });
  const data = await response.json();
  alert(JSON.stringify(data, null, 2));
}

async function loadTrainingTasks() {
  const response = await fetch('/training/tasks', {
    headers: getHeaders(),
  });
  const data = await response.json();
  const list = data.tasks || [];
  const container = document.getElementById('trainingList');
  container.innerHTML = list.map(task => `
    <div style="margin-bottom: 12px; padding: 10px; background: #222; border-radius: 8px;">
      <strong>${task.title}</strong><br />
      <p>${task.description}</p>
      <button onclick="executeTraining('${task.id}')">Run Task</button>
    </div>
  `).join('');
}

async function executeTraining(taskId) {
  const response = await fetch('/training/execute', {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ task_id: taskId }),
  });
  const data = await response.json();
  document.getElementById('trainingResult').textContent = JSON.stringify(data, null, 2);
}
window.onload = () => {
  updateAuthStatus();
  checkSandboxStatus();
};
