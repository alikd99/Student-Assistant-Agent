# 🎓 مساعد الطالب الذكي — Smart Student Assistant

Upload any study material and instantly get answers, summaries, flashcards, and exam questions — powered by free AI.

**Supports:** PDF · PPTX · DOCX &nbsp;|&nbsp; **Languages:** Arabic & English

---

## Requirements

Before you start, install these two free tools:

| Tool | Download | Note |
|------|----------|-------|
| Python 3.10+ | [python.org](https://www.python.org/downloads/) | ✅ Check **"Add Python to PATH"** during install |
| Node.js (LTS) | [nodejs.org](https://nodejs.org/) | Choose the LTS version |

---

## Installation (First Time Only)

```bash
# 1. Clone the repo
git clone https://github.com/your-username/student-assistant.git
cd student-assistant

# 2. Run setup
setup.bat
```

That's it. Setup installs all Python and frontend dependencies automatically.

---

## Running the App

```bash
start.bat
```

On first launch, you'll be asked to enter a **free Groq API key**:

```
============================================================
             FREE AI API KEY REQUIRED
============================================================

 HOW TO GET YOUR FREE KEY (takes 2 minutes):

   1. Go to:  https://console.groq.com
   2. Click "Sign Up" and create a free account
   3. Click "API Keys" in the left menu
   4. Click "Create API Key", give it any name
   5. Copy the key (starts with: gsk_...)
   6. Paste it here and press Enter
```

The key is saved locally on your device and never shared.

After that, the app opens automatically at **http://localhost:5173**

---

## Features

| Feature | Description |
|---------|-------------|
| 💬 Q&A | Ask any question about your document |
| 📝 Summary | Get a structured summary of the content |
| 🃏 Flashcards | Auto-generate 15–20 study flashcards |
| 📋 Exam Questions | Generate MCQ + True/False questions |

---

## How It Works

```
Your file (PDF/PPTX/DOCX)
        ↓
  Text extraction (local)
        ↓
  Split into chunks + embed (local)
        ↓
  Stored in ChromaDB (local, on your device)
        ↓
  Your question → find relevant chunks (local)
        ↓
  Send chunks + question to Groq AI (free API)
        ↓
  Answer returned to you
```

Your files **never leave your device** — only small text chunks are sent to Groq for AI processing.

---

## Stopping the App

Close the two terminal windows that open when you run `start.bat`.

---

## Troubleshooting

**"Setup not complete" error**
→ Run `setup.bat` first before `start.bat`

**"Invalid API key" error**
→ Delete the `GROQ_API_KEY=` line from `.env` and restart `start.bat` to re-enter your key

**Backend not starting**
→ Make sure port 8000 is not used by another app

**Frontend not loading**
→ Make sure port 5173 is not used by another app
