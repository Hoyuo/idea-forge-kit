/**
 * IdeaForge Dashboard Client
 * Real-time progress visualization
 */

// State
let currentPrdId = null;
let ws = null;

// API Base URL
const API_BASE = '/api';

// DOM Elements
const elements = {
  connectionStatus: document.getElementById('connectionStatus'),
  prdList: document.getElementById('prdList'),
  detailSection: document.getElementById('detailSection'),
  detailTitle: document.getElementById('detailTitle'),
  tasksList: document.getElementById('tasksList'),
  progressInfo: document.getElementById('progressInfo'),
  diagramsList: document.getElementById('diagramsList'),
  diagramPreview: document.getElementById('diagramPreview'),
  lastUpdate: document.getElementById('lastUpdate')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initWebSocket();
  refreshAll();

  // Auto-refresh every 30 seconds
  setInterval(refreshAll, 30000);
});

/**
 * Initialize WebSocket connection
 */
function initWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}`;

  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    updateConnectionStatus('connected');
  };

  ws.onclose = () => {
    updateConnectionStatus('disconnected');
    // Reconnect after 5 seconds
    setTimeout(initWebSocket, 5000);
  };

  ws.onerror = () => {
    updateConnectionStatus('disconnected');
  };

  ws.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data);
      handleWebSocketMessage(message);
    } catch (err) {
      console.error('WebSocket message parse error:', err);
    }
  };
}

/**
 * Handle WebSocket messages
 */
function handleWebSocketMessage(message) {
  if (message.type === 'file_change') {
    // Refresh data on file change
    refreshAll();

    // If viewing a specific PRD, refresh its details
    if (currentPrdId) {
      loadPrdDetails(currentPrdId);
    }
  }
}

/**
 * Update connection status indicator
 */
function updateConnectionStatus(status) {
  const statusDot = elements.connectionStatus.querySelector('.status-dot');
  const statusText = elements.connectionStatus.querySelector('.status-text');

  statusDot.className = 'status-dot';

  switch (status) {
    case 'connected':
      statusDot.classList.add('connected');
      statusText.textContent = 'Connected';
      break;
    case 'disconnected':
      statusDot.classList.add('disconnected');
      statusText.textContent = 'Disconnected';
      break;
    default:
      statusText.textContent = 'Connecting...';
  }
}

/**
 * Refresh all data
 */
async function refreshAll() {
  await Promise.all([
    loadSummary(),
    loadPrdList()
  ]);

  updateLastUpdate();
}

/**
 * Load summary statistics
 */
async function loadSummary() {
  try {
    const response = await fetch(`${API_BASE}/summary`);
    const data = await response.json();

    // Update summary cards
    document.querySelector('#totalPrds .summary-value').textContent = data.totalPrds;
    document.querySelector('#completedPrds .summary-value').textContent = data.completedPrds;
    document.querySelector('#inProgressPrds .summary-value').textContent = data.inProgressPrds;
    document.querySelector('#testStats .summary-value').textContent =
      data.totalTests > 0 ? `${data.testPassRate}%` : '-';
  } catch (err) {
    console.error('Failed to load summary:', err);
  }
}

/**
 * Load PRD list
 */
async function loadPrdList() {
  try {
    const response = await fetch(`${API_BASE}/prds`);
    const prds = await response.json();

    if (prds.length === 0) {
      elements.prdList.innerHTML = `
        <div class="empty-state">
          No PRDs found. Create one with <code>/forge:idea</code>
        </div>
      `;
      return;
    }

    elements.prdList.innerHTML = prds.map(prd => createPrdCard(prd)).join('');
  } catch (err) {
    console.error('Failed to load PRDs:', err);
    elements.prdList.innerHTML = `
      <div class="empty-state">Failed to load PRDs</div>
    `;
  }
}

/**
 * Create PRD card HTML
 */
function createPrdCard(prd) {
  const progress = prd.totalTasks > 0
    ? Math.round((prd.completedTasks / prd.totalTasks) * 100)
    : 0;

  const statusClass = getStatusClass(prd.status);
  const statusLabel = getStatusLabel(prd.status);
  const phaseHtml = prd.currentPhase ? createPhaseHtml(prd.currentPhase) : '';

  return `
    <div class="prd-card ${currentPrdId === prd.id ? 'active' : ''}"
         onclick="selectPrd('${prd.id}')">
      <span class="prd-id">${prd.id}</span>
      <span class="prd-title">${prd.title}</span>
      <div class="prd-progress">
        <div class="progress-bar">
          <div class="progress-fill" style="width: ${progress}%"></div>
        </div>
        <span class="progress-text">${progress}%</span>
      </div>
      ${phaseHtml}
      <span class="prd-status ${statusClass}">${statusLabel}</span>
    </div>
  `;
}

/**
 * Create TDD phase HTML
 */
function createPhaseHtml(phase) {
  const phaseClass = phase.toLowerCase();
  const phaseIcon = getPhaseIcon(phase);

  return `
    <span class="tdd-phase ${phaseClass}">
      ${phaseIcon} ${phase.toUpperCase()}
    </span>
  `;
}

/**
 * Get phase icon
 */
function getPhaseIcon(phase) {
  switch (phase?.toLowerCase()) {
    case 'red': return '🔴';
    case 'green': return '🟢';
    case 'refactor': return '🔵';
    default: return '';
  }
}

/**
 * Get status class
 */
function getStatusClass(status) {
  switch (status) {
    case 'completed':
    case 'all_features_complete':
      return 'completed';
    case 'in_progress':
    case 'building':
      return 'in_progress';
    default:
      return 'pending';
  }
}

/**
 * Get status label
 */
function getStatusLabel(status) {
  switch (status) {
    case 'completed':
    case 'all_features_complete':
      return 'Complete';
    case 'in_progress':
    case 'building':
      return 'Building';
    case 'pending':
      return 'Pending';
    default:
      return status;
  }
}

/**
 * Select a PRD to view details
 */
function selectPrd(prdId) {
  currentPrdId = prdId;
  elements.detailSection.style.display = 'block';
  loadPrdDetails(prdId);

  // Update active state in list
  document.querySelectorAll('.prd-card').forEach(card => {
    card.classList.remove('active');
  });
  event.currentTarget.classList.add('active');
}

/**
 * Close detail panel
 */
function closeDetail() {
  currentPrdId = null;
  elements.detailSection.style.display = 'none';

  // Remove active state from list
  document.querySelectorAll('.prd-card').forEach(card => {
    card.classList.remove('active');
  });
}

/**
 * Load PRD details
 */
async function loadPrdDetails(prdId) {
  elements.detailTitle.textContent = `PRD: ${prdId}`;

  await Promise.all([
    loadTasks(prdId),
    loadProgress(prdId),
    loadDiagrams(prdId)
  ]);
}

/**
 * Load tasks for PRD
 */
async function loadTasks(prdId) {
  try {
    const response = await fetch(`${API_BASE}/prds/${prdId}/tasks`);
    const data = await response.json();

    if (!data.tasks || data.tasks.length === 0) {
      elements.tasksList.innerHTML = `
        <div class="empty-state">
          No tasks yet. Run <code>/forge:analyze ${prdId}</code>
        </div>
      `;
      return;
    }

    elements.tasksList.innerHTML = data.tasks.map(task => `
      <div class="task-item">
        <span class="task-status">${getTaskIcon(task.status)}</span>
        <div class="task-info">
          <div class="task-id">${task.id}</div>
          <div class="task-title">${task.title || task.description || task.id}</div>
        </div>
        ${task.phase ? createPhaseHtml(task.phase) : ''}
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load tasks:', err);
    elements.tasksList.innerHTML = `
      <div class="empty-state">Failed to load tasks</div>
    `;
  }
}

/**
 * Get task status icon
 */
function getTaskIcon(status) {
  switch (status) {
    case 'completed': return '✅';
    case 'in_progress': return '🔨';
    case 'pending': return '⏳';
    default: return '○';
  }
}

/**
 * Load progress/checkpoint
 */
async function loadProgress(prdId) {
  try {
    const response = await fetch(`${API_BASE}/prds/${prdId}/progress`);
    const progress = await response.json();

    const completedCount = progress.completed_tasks?.length || 0;
    const pendingCount = progress.pending_tasks?.length || 0;
    const currentTask = progress.current_task || '-';
    const currentPhase = progress.current_phase || '-';

    let html = `
      <div class="progress-stat">
        <div class="progress-stat-label">Current Task</div>
        <div class="progress-stat-value">${currentTask}</div>
      </div>
      <div class="progress-stat">
        <div class="progress-stat-label">Current Phase</div>
        <div class="progress-stat-value">${currentPhase !== '-' ? getPhaseIcon(currentPhase) + ' ' + currentPhase.toUpperCase() : '-'}</div>
      </div>
      <div class="progress-stat">
        <div class="progress-stat-label">Completed Tasks</div>
        <div class="progress-stat-value">${completedCount}</div>
      </div>
      <div class="progress-stat">
        <div class="progress-stat-label">Pending Tasks</div>
        <div class="progress-stat-value">${pendingCount}</div>
      </div>
    `;

    // Add test summary if available
    if (progress.test_summary) {
      const ts = progress.test_summary;
      html += `
        <div class="test-summary" style="grid-column: 1 / -1;">
          <div class="test-stat">
            <span class="test-stat-value">${ts.total || 0}</span>
            <span class="test-stat-label">Total Tests</span>
          </div>
          <div class="test-stat">
            <span class="test-stat-value passed">${ts.passed || 0}</span>
            <span class="test-stat-label">Passed</span>
          </div>
          <div class="test-stat">
            <span class="test-stat-value failed">${ts.failed || 0}</span>
            <span class="test-stat-label">Failed</span>
          </div>
          <div class="test-stat">
            <span class="test-stat-value">${ts.coverage || 0}%</span>
            <span class="test-stat-label">Coverage</span>
          </div>
        </div>
      `;
    }

    elements.progressInfo.innerHTML = html;
  } catch (err) {
    console.error('Failed to load progress:', err);
    elements.progressInfo.innerHTML = `
      <div class="empty-state">Failed to load progress</div>
    `;
  }
}

/**
 * Load diagrams for PRD
 */
async function loadDiagrams(prdId) {
  try {
    const response = await fetch(`${API_BASE}/prds/${prdId}/diagrams`);
    const diagrams = await response.json();

    if (!diagrams || diagrams.length === 0) {
      elements.diagramsList.innerHTML = `
        <div class="empty-state">
          No diagrams yet. Run <code>/forge:design ${prdId}</code>
        </div>
      `;
      elements.diagramPreview.innerHTML = `
        <div class="empty-state">No diagrams available</div>
      `;
      return;
    }

    elements.diagramsList.innerHTML = diagrams.map(d => `
      <button class="diagram-btn" onclick="loadDiagram('${prdId}', '${d.name}', this)">
        ${d.name}
      </button>
    `).join('');

    elements.diagramPreview.innerHTML = `
      <div class="empty-state">Select a diagram to preview</div>
    `;
  } catch (err) {
    console.error('Failed to load diagrams:', err);
    elements.diagramsList.innerHTML = `
      <div class="empty-state">Failed to load diagrams</div>
    `;
  }
}

/**
 * Load and render a diagram
 */
async function loadDiagram(prdId, diagramName, btn) {
  try {
    // Update active button
    document.querySelectorAll('.diagram-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    // Show loading
    elements.diagramPreview.innerHTML = `
      <div class="loading">Loading diagram...</div>
    `;

    // Fetch diagram source
    const sourceResponse = await fetch(`${API_BASE}/prds/${prdId}/diagrams/${diagramName}`);
    const sourceData = await sourceResponse.json();

    if (!sourceData.content) {
      elements.diagramPreview.innerHTML = `
        <div class="empty-state">Diagram content not found</div>
      `;
      return;
    }

    // Render via PlantUML server
    const renderResponse = await fetch(`${API_BASE}/render-plantuml`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source: sourceData.content })
    });
    const renderData = await renderResponse.json();

    if (renderData.svg) {
      elements.diagramPreview.innerHTML = `
        <img src="${renderData.svg}" alt="${diagramName}" />
      `;
    } else {
      elements.diagramPreview.innerHTML = `
        <div class="empty-state">Failed to render diagram</div>
      `;
    }
  } catch (err) {
    console.error('Failed to load diagram:', err);
    elements.diagramPreview.innerHTML = `
      <div class="empty-state">Failed to load diagram</div>
    `;
  }
}

/**
 * Switch between tabs
 */
function switchTab(tabName) {
  // Update tab buttons
  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.toggle('active', tab.dataset.tab === tabName);
  });

  // Update tab panels
  document.querySelectorAll('.tab-panel').forEach(panel => {
    panel.classList.toggle('active', panel.id === `${tabName}Panel`);
  });
}

/**
 * Update last update timestamp
 */
function updateLastUpdate() {
  const now = new Date();
  const timeStr = now.toLocaleTimeString();
  elements.lastUpdate.textContent = `Last update: ${timeStr}`;
}
