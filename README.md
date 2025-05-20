# 💬 Socket-Chat

Ein einfaches Chatprogramm in Python mit einem ausfallsicheren Server.

## 📌 Projektübersicht

**Socket-Chat** ist eine Python-basierte Client-Server-Chat-Anwendung, die es mehreren Clients ermöglicht, Nachrichten in Echtzeit über ein zentrales Serversystem auszutauschen. Der Server ist so konzipiert, dass er stabil läuft und Verbindungsabbrüche einzelner Clients verkraftet.

## 🧰 Funktionen

- Mehrbenutzer-Chat über TCP/IP
- Serverseitiges Broadcasting von Nachrichten an alle verbundenen Clients
- Robuste Fehlerbehandlung bei Verbindungsabbrüchen
- Konsolenbasierte Benutzeroberfläche für einfache Bedienung

## 🛠️ Anforderungen

- Python 3.6 oder höher

## 🚀 Installation und Ausführung

1. **Repository klonen:**

   ```bash
   git clone https://github.com/duhan2/Socket-Chat.git
   cd Socket-Chat


2. **Server starten:**

   ```bash
   python server.py
   ```

   Der Server lauscht standardmäßig auf Port 12345. Stelle sicher, dass dieser Port nicht von einer anderen Anwendung belegt ist.

3. **Client starten:**

   In einem neuen Terminalfenster:

   ```bash
   python client.py
   ```

   Folge den Anweisungen, um einen Benutzernamen einzugeben und dem Chat beizutreten.

## 🗂️ Projektstruktur

```bash
Socket-Chat/
├── client.py       # Client-Anwendung
├── server.py       # Server-Anwendung
└── README.md       # Projektdokumentation
```

## 📄 Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).


## 📬 Kontakt

Projekt von [@duhan2](https://github.com/duhan2)

---

*Made with ❤️ in Python*

```

