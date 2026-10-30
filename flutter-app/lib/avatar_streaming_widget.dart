import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

/// Flutter Widget for Sky Meilin OS Overlay Avatar Streaming & Publishing
class AvatarStreamingWidget extends StatefulWidget {
  final String backendUrl;
  const AvatarStreamingWidget({Key? key, this.backendUrl = 'http://localhost:8000'}) : super(key: key);

  @override
  _AvatarStreamingWidgetState createState() => _AvatarStreamingWidgetState();
}

class _AvatarStreamingWidgetState extends State<AvatarStreamingWidget> {
  final TextEditingController _promptController = TextEditingController();
  final List<String> _textBuffer = [];
  bool _isStreaming = false;
  String _statusMessage = 'Bereit';

  Future<void> _startStreaming() async {
    final prompt = _promptController.text.trim();
    if (prompt.isEmpty) return;

    setState(() {
      _isStreaming = true;
      _textBuffer.clear();
      _statusMessage = 'Verbinde mit Avatar Streaming Endpoint...';
    });

    try {
      final request = http.Request('POST', Uri.parse('${widget.backendUrl}/stream'));
      request.headers['Content-Type'] = 'application/json';
      request.body = jsonEncode({'prompt': prompt});

      final response = await request.send();

      response.stream
          .transform(utf8.decoder)
          .transform(const LineSplitter())
          .listen((String line) {
        if (line.startsWith('data: ')) {
          final jsonData = line.substring(6).trim();
          if (jsonData.isNotEmpty) {
            final Map<String, dynamic> event = jsonDecode(jsonData);
            _handleStreamEvent(event);
          }
        }
      }, onDone: () {
        setState(() {
          _isStreaming = false;
          _statusMessage = 'Stream beendet.';
        });
      }, onError: (error) {
        setState(() {
          _isStreaming = false;
          _statusMessage = 'Fehler: $error';
        });
      });
    } catch (e) {
      setState(() {
        _isStreaming = false;
        _statusMessage = 'Verbindungsfehler: $e';
      });
    }
  }

  void _handleStreamEvent(Map<String, dynamic> event) {
    setState(() {
      final type = event['type'];
      if (type == 'text') {
        _textBuffer.add(event['content'] ?? '');
      } else if (type == 'status') {
        _statusMessage = event['content'] ?? '';
      } else if (type == 'avatar_sync') {
        // Sync Audio / Video Frame
        debugPrint('Avatar Sync: Frame ${event['video_frame_id']}');
      }
    });
  }

  Future<void> _publishContent() async {
    final content = _textBuffer.join();
    if (content.isEmpty) return;

    final response = await http.post(
      Uri.parse('${widget.backendUrl}/publish/wordpress'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'title': 'Sky Meilin Clip: ${_promptController.text}',
        'content': content,
        'status': 'publish'
      }),
    );

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Veröffentlichung getriggert: ${response.statusCode}')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.black.withOpacity(0.85),
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          // Avatar Display Overlay Area
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                border: Border.all(color: Colors.cyanAccent),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Stack(
                children: [
                  Center(
                    child: Icon(
                      Icons.account_circle,
                      size: 120,
                      color: _isStreaming ? Colors.cyanAccent : Colors.grey,
                    ),
                  ),
                  Positioned(
                    bottom: 12,
                    left: 12,
                    right: 12,
                    child: Text(
                      _textBuffer.join(),
                      style: const TextStyle(color: Colors.white, fontSize: 16),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          Text(_statusMessage, style: const TextStyle(color: Colors.cyanAccent)),
          const SizedBox(height: 12),
          // Input & Controls
          Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _promptController,
                  style: const TextStyle(color: Colors.white),
                  decoration: const InputDecoration(
                    hintText: 'Befehl / Eingabe an Sky Meilin...',
                    hintStyle: TextStyle(color: Colors.white54),
                  ),
                ),
              ),
              IconButton(
                icon: const Icon(Icons.send, color: Colors.cyanAccent),
                onPressed: _isStreaming ? null : _startStreaming,
              ),
              IconButton(
                icon: const Icon(Icons.publish, color: Colors.greenAccent),
                onPressed: _publishContent,
              ),
            ],
          ),
        ],
      ),
    );
  }
}
