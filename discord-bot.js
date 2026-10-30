import { Client, GatewayIntentBits, EmbedBuilder } from 'discord.js';
import { Ollama } from 'ollama';

// Discord Client erstellen
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

// Ollama Client
const ollama = new Ollama({
  host: process.env.OLLAMA_HOST || 'http://127.0.0.1:11434',
});

// Support-System-Prompt
const systemPrompt = `Du bist SkyOS Support, ein freundlicher und kompetenter Support-Assistent für das SkyOS Framework. 

Deine Aufgaben:
- Beantworte Fragen zu SkyOS, den 15 Departments, Docker-Setup, und MCP-Integration
- Hilf bei technischen Problemen mit der Installation und Konfiguration
- Erkläre die Architektur des Frameworks in einfacher Sprache
- Bleibe sachlich, freundlich und hilfreich

Wichtige Informationen:
- SkyOS ist ein Framework mit 15 Departments (MCP+CIP-Protokolle)
- Das Framework läuft in Docker-Containern (Chat, MCP-Bridge, Payment, Bridge)
- Ollama wird für lokale LLM-Funktionen verwendet
- Die Flutter-App ist das mobile Frontend mit Vision AI und Discord-Gateway

Antworte immer auf der Sprache des Nutzers. Wenn du eine Frage nicht beantworten kannst, sage es ehrlich und biete an, weiterzuhelfen.`;

// Konversationshistorie pro Kanal (einfaches Gedächtnis)
const conversationHistory = new Map();

async function getOllamaResponse(channelId, userMessage) {
  // Historie für diesen Kanal laden oder erstellen
  if (!conversationHistory.has(channelId)) {
    conversationHistory.set(channelId, [
      { role: 'system', content: systemPrompt },
    ]);
  }

  const history = conversationHistory.get(channelId);
  
  // Nutzer-Nachricht hinzufügen
  history.push({ role: 'user', content: userMessage });

  // Historie auf letzte 10 Nachrichten begrenzen (plus System)
  if (history.length > 11) {
    history.splice(1, history.length - 11);
  }

  try {
    const response = await ollama.chat({
      model: process.env.OLLAMA_MODEL || 'llama3',
      messages: history,
      stream: false,
    });

    const assistantReply = response.message.content;

    // Antwort zur Historie hinzufügen
    history.push({ role: 'assistant', content: assistantReply });

    // Historie wieder begrenzen
    if (history.length > 11) {
      history.splice(1, history.length - 11);
    }

    return assistantReply;
  } catch (error) {
    console.error('[Ollama Fehler]:', error.message);
    return null;
  }
}

client.on('ready', () => {
  console.log('================================================');
  console.log(`🤖 SkyOS Support-Bot ist online als ${client.user.tag}`);
  console.log(`🔗 Verbunden mit Ollama auf ${process.env.OLLAMA_HOST || 'http://127.0.0.1:11434'}`);
  console.log(`📦 Modell: ${process.env.OLLAMA_MODEL || 'llama3'}`);
  console.log('================================================');
});

client.on('messageCreate', async (message) => {
  // Ignoriere Bot-Nachrichten
  if (message.author.bot) return;

  // Nur auf direkte Erwähnungen oder DMs antworten
  const isMentioned = message.mentions.users.has(client.user.id);
  const isDM = message.channel.type === 0; // DM Kanal

  if (!isMentioned && !isDM) return;

  // Bestätigungsnachricht
  const thinkingMessage = await message.reply('⏳ *Verarbeite deine Anfrage...*');

  try {
    const userContent = message.content.replace(new RegExp(`<@!?${client.user.id}>`, 'g'), '').trim();
    
    if (!userContent) {
      await thinkingMessage.edit('❓ *Bitte stelle eine Frage oder beschreibe dein Problem.*');
      return;
    }

    // Antwort von Ollama holen
    const reply = await getOllamaResponse(message.channel.id, userContent);

    if (reply) {
      // Antwort in Embed formatieren (max 2000 Zeichen)
      const embed = new EmbedBuilder()
        .setTitle('🛠️ SkyOS Support')
        .setDescription(reply.length > 2000 ? reply.substring(0, 1997) + '...' : reply)
        .setColor(0x38BDF8)
        .setFooter({ text: 'Angetrieben von Ollama LLM' })
        .setTimestamp();

      await thinkingMessage.edit({ content: '', embeds: [embed] });
    } else {
      await thinkingMessage.edit('⚠️ *Fehler bei der Antwortgenerierung. Bitte versuche es später erneut.*');
    }
  } catch (error) {
    console.error('[Discord Fehler]:', error.message);
    await thinkingMessage.edit('❌ *Ein unerwarteter Fehler ist aufgetreten.*');
  }
});

// Slash-Befehl: /help
client.on('interactionCreate', async (interaction) => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === 'help') {
    const embed = new EmbedBuilder()
      .setTitle('🛠️ SkyOS Support-Bot')
      .setDescription('Ich bin dein Support-Assistent für SkyOS Framework.')
      .addFields(
        { name: '💬 Chat', value: 'Erwähne mich (`@SkyOS Support`) oder schreibe mir eine DM.' },
        { name: '📚 Dokumentation', value: 'Frag mich nach Departments, Setup, oder Architektur.' },
        { name: '🔧 Hilfe', value: 'Beschreibe dein Problem, ich helfe dir weiter.' }
      )
      .setColor(0x38BDF8)
      .setTimestamp();

    await interaction.reply({ embeds: [embed], ephemeral: false });
  }
});

// Bot starten
const token = process.env.DISCORD_BOT_TOKEN;
if (!token) {
  console.error('❌ Fehler: DISCORD_BOT_TOKEN ist nicht gesetzt!');
  console.error('   Setze die Umgebungsvariable in deiner .env Datei.');
  process.exit(1);
}

client.login(token);
