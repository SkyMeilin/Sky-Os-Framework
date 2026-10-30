import 'dart:convert';
import 'package:http/http.dart' as http;

/// MCP-Client für SkyOS Bridge
/// Verbindet die Flutter-App mit der Bridge (Port 3000)
class McpClient {
  final String bridgeUrl;
  final http.Client _client;

  McpClient({
    String baseUrl = 'http://localhost:3000',
    http.Client? client,
  })  : bridgeUrl = baseUrl,
        _client = client ?? http.Client();

  /// Verfügbare MCP-Tools auflisten
  Future<List<McpTool>> getTools() async {
    final response = await _client.get(
      Uri.parse('$bridgeUrl/api/mcp/tools'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final toolsList = data['result']['tools'] as List;
      return toolsList.map((t) => McpTool.fromJson(t)).toList();
    } else {
      throw Exception('Fehler beim Laden der Tools: ${response.statusCode}');
    }
  }

  /// MCP-Tool ausführen
  Future<McpResult> callTool(String toolName, [Map<String, dynamic> arguments = const {}]) async {
    final response = await _client.post(
      Uri.parse('$bridgeUrl/api/mcp/call'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'tool': toolName,
        'arguments': arguments,
      }),
    );

    if (response.statusCode == 200) {
      return McpResult.fromJson(jsonDecode(response.body));
    } else {
      final error = jsonDecode(response.body);
      throw Exception('Tool-Aufruf fehlgeschlagen: ${error['error']['message']}');
    }
  }

  /// Discord-Event senden
  Future<bool> sendDiscordEvent(String action, [Map<String, dynamic> payload = const {}]) async {
    final response = await _client.post(
      Uri.parse('$bridgeUrl/api/discord'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'action': action,
        'payload': payload,
        'timestamp': DateTime.now().toIso8601String(),
      }),
    );

    return response.statusCode == 200;
  }

  /// Befehl an Ollama senden
  Future<String> sendCommand(String command, {String model = 'llama3'}) async {
    final response = await _client.post(
      Uri.parse('$bridgeUrl/api/command'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'command': command,
        'model': model,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['message'] as String;
    } else {
      throw Exception('Befehl fehlgeschlagen: ${response.statusCode}');
    }
  }

  void dispose() {
    _client.close();
  }
}

/// MCP-Tool-Definition
class McpTool {
  final String name;
  final String description;
  final Map<String, dynamic> parameters;

  McpTool({
    required this.name,
    required this.description,
    required this.parameters,
  });

  factory McpTool.fromJson(Map<String, dynamic> json) {
    return McpTool(
      name: json['name'] as String,
      description: json['description'] as String,
      parameters: json['parameters'] as Map<String, dynamic>,
    );
  }
}

/// MCP-Ergebnis
class McpResult {
  final String tool;
  final bool success;
  final Map<String, dynamic> data;

  McpResult({
    required this.tool,
    required this.success,
    required this.data,
  });

  factory McpResult.fromJson(Map<String, dynamic> json) {
    return McpResult(
      tool: json['result']['tool'] as String,
      success: json['result']['success'] as bool,
      data: json['result']['data'] as Map<String, dynamic>,
    );
  }
}
