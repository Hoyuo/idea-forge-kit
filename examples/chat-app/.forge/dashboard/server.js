/**
 * IdeaForge Dashboard Server
 * Real-time progress visualization for IdeaForge workflow
 */

const express = require('express');
const { WebSocketServer } = require('ws');
const fs = require('fs');
const path = require('path');
const http = require('http');

const app = express();
const PORT = process.env.PORT || 20555;

// Project root (parent of .forge)
const PROJECT_ROOT = path.resolve(__dirname, '../..');
const FORGE_DIR = path.join(PROJECT_ROOT, '.forge');

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// CORS for development
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});

/**
 * Helper: Read JSON file safely
 */
function readJsonFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
  } catch (err) {
    console.error(`Error reading ${filePath}:`, err.message);
  }
  return null;
}

/**
 * Helper: Read markdown file
 */
function readMarkdownFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return fs.readFileSync(filePath, 'utf8');
    }
  } catch (err) {
    console.error(`Error reading ${filePath}:`, err.message);
  }
  return null;
}

/**
 * Helper: Parse PRD frontmatter
 */
function parsePrdFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (match) {
    const frontmatter = {};
    match[1].split('\n').forEach(line => {
      const [key, ...valueParts] = line.split(':');
      if (key && valueParts.length) {
        frontmatter[key.trim()] = valueParts.join(':').trim().replace(/^["']|["']$/g, '');
      }
    });
    return frontmatter;
  }
  return {};
}

/**
 * API: Get all PRDs
 */
app.get('/api/prds', (req, res) => {
  const prdsDir = path.join(FORGE_DIR, 'prds');
  const prds = [];

  if (fs.existsSync(prdsDir)) {
    const files = fs.readdirSync(prdsDir).filter(f => f.endsWith('.md'));

    files.forEach(file => {
      const content = readMarkdownFile(path.join(prdsDir, file));
      if (content) {
        const frontmatter = parsePrdFrontmatter(content);
        const id = frontmatter.id || file.replace('.md', '');

        // Get progress
        const progressFile = path.join(FORGE_DIR, 'progress', id, 'checkpoint.json');
        const progress = readJsonFile(progressFile) || {};

        // Get tasks
        const tasksFile = path.join(FORGE_DIR, 'tasks', id, 'tasks.json');
        const tasks = readJsonFile(tasksFile) || {};

        prds.push({
          id,
          title: frontmatter.title || id,
          status: progress.status || frontmatter.status || 'pending',
          priority: frontmatter.priority || 'medium',
          created: frontmatter.created,
          currentTask: progress.current_task,
          currentPhase: progress.current_phase,
          completedTasks: progress.completed_tasks?.length || 0,
          totalTasks: tasks.total_tasks || 0,
          testSummary: progress.test_summary || null
        });
      }
    });
  }

  res.json(prds);
});

/**
 * API: Get PRD details
 */
app.get('/api/prds/:id', (req, res) => {
  const { id } = req.params;
  const prdFile = path.join(FORGE_DIR, 'prds', `${id}.md`);

  if (!fs.existsSync(prdFile)) {
    return res.status(404).json({ error: 'PRD not found' });
  }

  const content = readMarkdownFile(prdFile);
  const frontmatter = parsePrdFrontmatter(content);

  // Get progress
  const progressFile = path.join(FORGE_DIR, 'progress', id, 'checkpoint.json');
  const progress = readJsonFile(progressFile) || {};

  // Get tasks
  const tasksFile = path.join(FORGE_DIR, 'tasks', id, 'tasks.json');
  const tasksData = readJsonFile(tasksFile) || { tasks: [] };

  res.json({
    id,
    title: frontmatter.title || id,
    status: progress.status || frontmatter.status || 'pending',
    priority: frontmatter.priority || 'medium',
    created: frontmatter.created,
    content,
    progress,
    tasks: tasksData.tasks || []
  });
});

/**
 * API: Get tasks for PRD
 */
app.get('/api/prds/:id/tasks', (req, res) => {
  const { id } = req.params;
  const tasksFile = path.join(FORGE_DIR, 'tasks', id, 'tasks.json');
  const progressFile = path.join(FORGE_DIR, 'progress', id, 'checkpoint.json');

  const tasksData = readJsonFile(tasksFile) || { tasks: [] };
  const progress = readJsonFile(progressFile) || {};

  // Enrich tasks with status
  const tasks = tasksData.tasks.map(task => ({
    ...task,
    status: progress.completed_tasks?.includes(task.id)
      ? 'completed'
      : progress.current_task === task.id
        ? 'in_progress'
        : 'pending',
    phase: progress.current_task === task.id ? progress.current_phase : null
  }));

  res.json({
    prdId: id,
    totalTasks: tasksData.total_tasks || tasks.length,
    tasks
  });
});

/**
 * API: Get progress/checkpoint
 */
app.get('/api/prds/:id/progress', (req, res) => {
  const { id } = req.params;
  const progressFile = path.join(FORGE_DIR, 'progress', id, 'checkpoint.json');

  const progress = readJsonFile(progressFile);
  if (!progress) {
    return res.json({
      prdId: id,
      status: 'not_started',
      completedTasks: [],
      pendingTasks: [],
      currentTask: null,
      currentPhase: null
    });
  }

  res.json(progress);
});

/**
 * API: List diagrams for PRD
 */
app.get('/api/prds/:id/diagrams', (req, res) => {
  const { id } = req.params;
  const diagramsDir = path.join(FORGE_DIR, 'design', id, 'diagrams');

  if (!fs.existsSync(diagramsDir)) {
    return res.json([]);
  }

  const diagrams = fs.readdirSync(diagramsDir)
    .filter(f => f.endsWith('.puml'))
    .map(f => ({
      name: f.replace('.puml', ''),
      file: f,
      path: path.join(diagramsDir, f)
    }));

  res.json(diagrams);
});

/**
 * API: Get diagram source
 */
app.get('/api/prds/:id/diagrams/:name', (req, res) => {
  const { id, name } = req.params;
  const diagramFile = path.join(FORGE_DIR, 'design', id, 'diagrams', `${name}.puml`);

  if (!fs.existsSync(diagramFile)) {
    return res.status(404).json({ error: 'Diagram not found' });
  }

  const content = readMarkdownFile(diagramFile);
  res.json({ name, content });
});

/**
 * API: Render PlantUML to SVG (proxy to PlantUML server)
 */
app.post('/api/render-plantuml', async (req, res) => {
  const { source } = req.body;

  if (!source) {
    return res.status(400).json({ error: 'No PlantUML source provided' });
  }

  // Encode for PlantUML server
  const encoded = Buffer.from(source).toString('base64');

  // Return URL to PlantUML server
  res.json({
    svg: `https://www.plantuml.com/plantuml/svg/~1${encoded}`,
    png: `https://www.plantuml.com/plantuml/png/~1${encoded}`
  });
});

/**
 * API: Get dashboard summary
 */
app.get('/api/summary', (req, res) => {
  const prdsDir = path.join(FORGE_DIR, 'prds');
  let totalPrds = 0;
  let completedPrds = 0;
  let inProgressPrds = 0;
  let totalTests = 0;
  let passedTests = 0;

  if (fs.existsSync(prdsDir)) {
    const files = fs.readdirSync(prdsDir).filter(f => f.endsWith('.md'));
    totalPrds = files.length;

    files.forEach(file => {
      const content = readMarkdownFile(path.join(prdsDir, file));
      if (content) {
        const frontmatter = parsePrdFrontmatter(content);
        const id = frontmatter.id || file.replace('.md', '');

        const progressFile = path.join(FORGE_DIR, 'progress', id, 'checkpoint.json');
        const progress = readJsonFile(progressFile) || {};

        if (progress.status === 'completed' || progress.status === 'all_features_complete') {
          completedPrds++;
        } else if (progress.current_task) {
          inProgressPrds++;
        }

        if (progress.test_summary) {
          totalTests += progress.test_summary.total || 0;
          passedTests += progress.test_summary.passed || 0;
        }
      }
    });
  }

  res.json({
    totalPrds,
    completedPrds,
    inProgressPrds,
    pendingPrds: totalPrds - completedPrds - inProgressPrds,
    totalTests,
    passedTests,
    failedTests: totalTests - passedTests,
    testPassRate: totalTests > 0 ? Math.round((passedTests / totalTests) * 100) : 0
  });
});

// Create HTTP server
const server = http.createServer(app);

// WebSocket for real-time updates
const wss = new WebSocketServer({ server });

wss.on('connection', (ws) => {
  console.log('Client connected');

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// Broadcast updates to all clients
function broadcastUpdate(type, data) {
  wss.clients.forEach(client => {
    if (client.readyState === 1) { // WebSocket.OPEN
      client.send(JSON.stringify({ type, data }));
    }
  });
}

// File watcher for real-time updates
try {
  const chokidar = require('chokidar');

  const watcher = chokidar.watch([
    path.join(FORGE_DIR, 'prds'),
    path.join(FORGE_DIR, 'tasks'),
    path.join(FORGE_DIR, 'progress'),
    path.join(FORGE_DIR, 'design')
  ], {
    ignoreInitial: true,
    persistent: true
  });

  watcher.on('all', (event, filePath) => {
    console.log(`File ${event}: ${filePath}`);
    broadcastUpdate('file_change', { event, path: filePath });
  });

  console.log('File watcher enabled');
} catch (err) {
  console.log('File watcher not available (chokidar not installed)');
}

// Start server
server.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🔥 IdeaForge Dashboard                                  ║
║                                                           ║
║   Server running at: http://localhost:${PORT}               ║
║                                                           ║
║   Features:                                               ║
║   ├── PRD List & Status                                   ║
║   ├── TDD Phase Visualization                             ║
║   ├── Test Results & Coverage                             ║
║   └── Diagram Preview                                     ║
║                                                           ║
║   Press Ctrl+C to stop the server.                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
  `);
});
