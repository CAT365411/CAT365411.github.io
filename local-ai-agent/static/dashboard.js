// Screen Stream WebSocket Connection
function initScreenStreamWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/screen`;
  const socket = new WebSocket(wsUrl);

  const streamImg = document.getElementById('screenStream');
  const statusBadge = document.getElementById('connectionStatus');

  socket.onopen = () => {
    if (statusBadge) {
      statusBadge.textContent = '● LIVE';
      statusBadge.className = 'text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-900/50 text-emerald-300 border border-emerald-700';
    }
  };

  socket.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data);
      if (message.type === 'frame' && message.data && streamImg) {
        streamImg.src = `data:image/jpeg;base64,${message.data}`;
      }
    } catch (err) {
      console.error('Error parsing frame:', err);
    }
  };

  socket.onclose = () => {
    if (statusBadge) {
      statusBadge.textContent = '○ OFFLINE (Reconnecting...)';
      statusBadge.className = 'text-xs font-semibold px-2.5 py-1 rounded-full bg-red-900/50 text-red-300 border border-red-700';
    }
    setTimeout(initScreenStreamWebSocket, 3000);
  };

  socket.onerror = (err) => {
    console.error('WebSocket Error:', err);
    socket.close();
  };
}

async function executeTaskPrompt() {
  const promptInput = document.getElementById('taskPrompt');
  const taskResult = document.getElementById('taskResult');
  const prompt = promptInput ? promptInput.value : '';

  if (!prompt.trim()) return;

  if (taskResult) {
    taskResult.classList.remove('hidden');
    taskResult.textContent = 'Running autonomous agent...';
  }

  try {
    const response = await fetch('/task/execute', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ prompt }),
    });
    const data = await response.json();
    if (taskResult) {
      taskResult.textContent = JSON.stringify(data, null, 2);
    }
  } catch (err) {
    if (taskResult) {
      taskResult.textContent = 'Execution Error: ' + err.message;
    }
  }
}

async function checkSandboxStatus() {
  try {
    const response = await fetch('/sandbox/status');
    const data = await response.json();
    const sandboxEl = document.getElementById('sandboxStatus');
    if (sandboxEl) sandboxEl.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    console.error('Failed to fetch sandbox status:', err);
  }
}

async function logout() {
  try {
    const response = await fetch('/logout', { method: 'POST' });
    const data = await response.json();
    if (data.status === 'logged_out') {
      window.location.href = '/login';
    }
  } catch (err) {
    console.error('Logout failed:', err);
  }
}

window.onload = () => {
  initScreenStreamWebSocket();
  checkSandboxStatus();
  const taskPrompt = document.getElementById('taskPrompt');
  if (taskPrompt) taskPrompt.focus();
};