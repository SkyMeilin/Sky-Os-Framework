# SkyOS Overlay – Flutter-App

Mobile App für SkyOS Framework mit **MCP-Integration**, **Vision AI** und **Discord-Gateway**.

## Architektur

```
flutter-app/
├── lib/
│   ├── mcp_client.dart      # MCP-Client für Bridge-Kommunikation
│   └── main.dart            # Hauptanwendung (wird später hinzugefügt)
├── pubspec.yaml             # Abhängigkeiten
└── README.md                # Diese Datei
```

## MCP-Client verwenden

Der `McpClient` verbindet die Flutter-App mit der SkyOS Bridge (Port 3000).

### Initialisierung

```dart
import 'package:skyos_overlay/mcp_client.dart';

final mcp = McpClient(baseUrl: 'http://localhost:3000');
```

### Verfügbare Tools auflisten

```dart
final tools = await mcp.getTools();
for (final tool in tools) {
  print('${tool.name}: ${tool.description}');
}
```

### Tool ausführen

```dart
// sky_os_execute: Befehl in Department ausführen
final result = await mcp.callTool('sky_os_execute', {
  'command': 'Status aller Departments',
  'department': 'Development',
  'model': 'llama3',
});

print(result.data['response']);
```

```dart
// discord_relay: Event an Discord senden
final result = await mcp.callTool('discord_relay', {
  'action': 'video_loaded',
  'payload': {'filename': 'video.mp4'},
});
```

```dart
// vision_analysis: Video analysieren
final result = await mcp.callTool('vision_analysis', {
  'videoPath': '/path/to/video.mp4',
  'mode': 'faces',
});
```

### Discord-Event direkt senden

```dart
final success = await mcp.sendDiscordEvent('video_loaded', {
  'filename': 'video.mp4',
  'duration': 120,
});
```

### Befehl an Ollama senden

```dart
final response = await mcp.sendCommand(
  'Was ist Sky OS?',
  model: 'llama3',
);
print(response);
```

## Bridge-Endpunkte

| Endpoint | Methode | Beschreibung |
|---|---|---|
| `/api/mcp/tools` | GET | MCP-Tools auflisten |
| `/api/mcp/call` | POST | MCP-Tool ausführen |
| `/api/discord` | POST | Discord-Event senden |
| `/api/command` | POST | Ollama-Chat |

## Voraussetzungen

1. **Flutter SDK** installiert (>=3.0.0)
2. **SkyOS Bridge** läuft auf `http://localhost:3000`
3. **Ollama** läuft lokal auf Port 11434

## App starten

```bash
cd flutter-app
flutter pub get
flutter run
```

## Joy AI Orchester

Die App ist vorbereitet für **Joy AI Orchester**-Integration. Das Orchester koordiniert:

- **MCP-Tools** über die Bridge
- **Vision AI** für Video-Analyse
- **Discord-Gateway** für Event-Sync
- **Spracherkennung** für Voice-Befehle

Die konkrete Implementierung des Orchesters erfolgt in `lib/main.dart` (wird später hinzugefügt).
