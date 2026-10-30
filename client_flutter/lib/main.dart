import 'package:flutter/material.dart';
import 'src/auth/github_auth.dart';
import 'src/scanner/scanner_page.dart';

void main() {
  runApp(const SkyOSApp());
}

class SkyOSApp extends StatelessWidget {
  const SkyOSApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SkyOS Open Core',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      themeMode: ThemeMode.system,
      home: const HomePage(),
      routes: {
        '/scanner': (context) => const ScannerPage(),
      },
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _authService = GitHubAuthService();

  @override
  void initState() {
    super.initState();
    _checkAuth();
  }

  Future<void> _checkAuth() async {
    final token = await _authService.getToken();
    if (token != null) {
      // User is authenticated
    }
  }

  Future<void> _handleLogin() async {
    final authUrl = await _authService.getAuthUrl();
    // Open auth URL in web view
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🛡️ SkyOS Open Core'),
        actions: [
          TextButton(
            onPressed: _handleLogin,
            child: const Text('Login'),
          ),
        ],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.shield, size: 80, color: Colors.blue),
              const SizedBox(height: 24),
              const Text(
                'SkyOS Open Core',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              const Text(
                'Behördenbescheid-Scanner & Notfall-Leitfäden',
                style: TextStyle(fontSize: 16, color: Colors.grey),
              ),
              const SizedBox(height: 48),
              _featureCard(
                icon: Icons.description,
                title: 'OCR-Bescheid-Scanner',
                subtitle: 'Behördenbescheide scannen und parsen',
                onTap: () {
                  Navigator.pushNamed(context, '/scanner');
                },
              ),
              const SizedBox(height: 16),
              _featureCard(
                icon: Icons.emergency,
                title: 'Notfall-Leitfäden',
                subtitle: 'OBG NRW §14 Notfallgenehmigungen',
                onTap: () {},
              ),
              const SizedBox(height: 16),
              _featureCard(
                icon: Icons.lock,
                title: 'DSGVO-Anonymizer',
                subtitle: 'Privacy-by-Design Telemetry',
                onTap: () {},
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _featureCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            children: [
              Icon(icon, size: 40, color: Colors.blue),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      subtitle,
                      style: const TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.arrow_forward_ios, size: 16),
            ],
          ),
        ),
      ),
    );
  }
}
