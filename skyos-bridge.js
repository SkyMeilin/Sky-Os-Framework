import express from 'express';
import cors from 'cors';
import { Ollama } from 'ollama';

const app = express();
const port = process.env.PORT || 3000;

// CORS Middleware — explizite Origin-Liste (kein Wildcard!)
app.use(cors({
  origin: [
    'http://localhost:3000',   // Next.js Dev
    'http://localhost:4200',   // Angular Dev Server
    'http://localhost:8080',   // Flutter Web Dev
    'http://localhost:8000',   // FastAPI Dev
  ],
  credentials: true,
}));
app.use(express.json());

// API-Key Authentifizierung Middleware
const API_KEY = process.env.SKYOS_API_KEY;
if (!API_KEY) {
  console.error('[FATAL] SKYOS_API_KEY environment variable is not set!');
  process.exit(1);
}

function verifyApiKey(req, res, next) {
  const key = req.headers['x-api-key'];
  if (!key) {
    return res.status(402).json({
      status: 'error',
      detail: 'Payment Required: Active SaaS license or valid API Key required.'
    });
  }
  if (key !== API_KEY) {
    return res.status(401).json({
      status: 'error',
      detail: 'Unauthorized: Invalid API Key provided.'
    });
  }
  next();
}

const ollama = new Ollama({ host: process.env.OLLAMA_HOST || 'http://127.0.0.1:11434' });

// MCP-Tools-Register (werd von der Flutter-App abgefragt)
const mcpTools = [
  {
    name: 'sky_os_execute',
    description: 'Führt einen Befehl im SkyOS Framework aus (15 Departments)',
    parameters: {
      type: 'object',
      properties: {
        command: { type: 'string', description: 'Der auszuführende Befehl' },
        department: { type: 'string', description: 'Ziel-Department (optional)' },
        model: { type: 'string', description: 'Ollama-Modell (Standard: llama3)' }
      },
      required: ['command']
    }
  },
  {
    name: 'discord_relay',
    description: 'Sendet ein Event an das Discord-Gateway',
    parameters: {
      type: 'object',
      properties: {
        action: { type: 'string', description: 'Aktionstyp (z.B. video_loaded, vision_analysis)' },
        payload: { type: 'object', description: 'Zusätzliche Daten' }
      },
      required: ['action']
    }
  },
  {
    name: 'vision_analysis',
    description: 'Startet eine Vision-AI-Analyse eines Videos',
    parameters: {
      type: 'object',
      properties: {
        videoPath: { type: 'string', description: 'Pfad zum Video' },
        mode: { type: 'string', description: 'Analyse-Modus (faces, gestures, silence)' }
      },
      required: ['videoPath']
    }
  }
];

// 1. Befehls-Endpoint (Ollama-Chat)
app.post('/api/command', verifyApiKey, async (req, res) => {
  const { command, model = 'llama3' } = req.body;
  console.log(`[SkyOS Core] Befehl empfangen: ${command}`);

  try {
    const response = await ollama.chat({
      model: model,
      messages: [{ role: 'user', content: command }],
    });
    res.json({ status: 'ok', message: response.message.content });
  } catch (err) {
    console.error(`[Ollama Fehler]:`, err.message);
    res.status(500).json({ status: 'error', error: err.message });
  }
});

// 2. Discord-Relay-Endpoint (für Flutter-App Events)
app.post('/api/discord', verifyApiKey, (req, res) => {
  const payload = req.body;
  console.log(`[Discord Relay] Event empfangen:`, JSON.stringify(payload, null, 2));

  // Hier können Events an Discord-Bot oder Webhooks weitergeleitet werden
  res.json({ status: 'success', relay: 'received', timestamp: new Date().toISOString() });
});

// 3. MCP-Tools auflisten
app.get('/api/mcp/tools', verifyApiKey, (req, res) => {
  res.json({
    jsonrpc: '2.0',
    result: {
      tools: mcpTools
    }
  });
});

// 4. MCP-Tool ausführen
app.post('/api/mcp/call', verifyApiKey, async (req, res) => {
  const { tool, arguments: toolArgs = {} } = req.body;
  console.log(`[MCP] Tool-Aufruf: ${tool}`, toolArgs);

  // Tool finden
  const toolDef = mcpTools.find(t => t.name === tool);
  if (!toolDef) {
    return res.status(404).json({
      jsonrpc: '2.0',
      error: { code: -32601, message: `Tool '${tool}' nicht gefunden` }
    });
  }

  try {
    let result;

    switch (tool) {
      case 'sky_os_execute': {
        const { command, department, model = 'llama3' } = toolArgs;
        const prompt = department
          ? `Department: ${department}\nBefehl: ${command}`
          : command;

        const response = await ollama.chat({
          model: model,
          messages: [{ role: 'user', content: prompt }],
        });

        result = {
          executed: true,
          department: department || 'all',
          response: response.message.content,
        };
        break;
      }

      case 'discord_relay': {
        const { action, payload } = toolArgs;
        console.log(`[MCP Discord Relay] Aktion: ${action}`, payload);
        result = {
          relayed: true,
          action: action,
          timestamp: new Date().toISOString(),
        };
        break;
      }

      case 'vision_analysis': {
        const { videoPath, mode = 'faces' } = toolArgs;
        console.log(`[MCP Vision] Analyse: ${videoPath} (Modus: ${mode})`);
        // Mock-Antwort – echte Vision-AI wird später implementiert
        result = {
          analyzed: true,
          video: videoPath,
          mode: mode,
          findings: [
            { type: 'face', confidence: 0.95, timestamp: '00:01:23' },
            { type: 'silence', duration: 3.2, timestamp: '00:02:10' }
          ],
          note: 'Mock-Ergebnis – Vision-AI wird später implementiert',
        };
        break;
      }

      default: {
        return res.status(400).json({
          jsonrpc: '2.0',
          error: { code: -32600, message: `Tool '${tool}' ist nicht implementiert` }
        });
      }
    }

    res.json({
      jsonrpc: '2.0',
      result: {
        tool: tool,
        success: true,
        data: result,
      },
    });
  } catch (err) {
    console.error(`[MCP Fehler] ${tool}:`, err.message);
    res.status(500).json({
      jsonrpc: '2.0',
      error: { code: -32000, message: err.message }
    });
  }
});

// 5. Health-Check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'SkyOS Bridge',
    version: '1.0.0',
    ollama: process.env.OLLAMA_HOST || 'http://127.0.0.1:11434',
    uptime: process.uptime(),
  });
});

app.listen(port, () => {
  console.log('================================================');
  console.log(`🚀 SkyOS Bridge aktiv auf http://localhost:${port}`);
  console.log(`🔗 Verbunden mit Ollama auf ${process.env.OLLAMA_HOST || 'http://127.0.0.1:11434'}`);
  console.log(`📦 MCP-Tools: ${mcpTools.map(t => t.name).join(', ')}`);
  console.log('================================================');
});
