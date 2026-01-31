
# 🌐 NetMon-AI: Intelligent Network Monitoring Platform

> **"Talk to your server."** > NetMon-AI transforms complex system administration into simple natural language conversations. Powered by **Groq Cloud** and **Llama 3.3**, it combines the power of a CLI with the intelligence of a modern LLM.

---

## 📖 Overview

**NetMon-AI** is a next-generation system administration tool designed to bridge the gap between manual command-line operations and intelligent automation. It provides a unified shell interface where you can monitor system health, audit file integrity, manage processes, and execute complex automation playbooks—all through natural language or native commands.

Unlike standard tools, NetMon-AI features a **Human-in-the-Loop (HITL) Security Protocol**, ensuring that AI suggestions for critical tasks (like killing processes or deleting files) require explicit administrator approval.

---

## ✨ Key Features

### 🧠 **Intelligent AI Core**

* **Natural Language Processing:** Built on `Llama-3.3-70b-versatile` and `NLTK`, allowing you to ask questions like *"Why is the system slow?"* or *"Kill all high-cpu processes."*
* **Context Awareness:** The AI knows your current directory, OS, and active system stats before answering.
* **Path Sanitization:** Automatically handles Windows/Linux path differences.

### 📊 **Live System Dashboard**

* **TUI Visualization:** A professional, real-time dashboard built with `Rich` showing CPU, Memory, Disk, and Network usage.
* **Visual Alerts:** Metrics turn **RED** automatically when they exceed critical thresholds.

### 🛡️ **Enterprise-Grade Security**

* **File Integrity Monitoring (FIM):** Detects unauthorized changes to critical files using SHA-256 hashing.
* **Audit Trail:** Every AI action—authorized or rejected—is logged permanently to `ai_audit.log` for compliance.
* **Risk Zones:** AI intents are classified into **Green** (Safe), **Yellow** (Caution), and **Red** (Critical/Blocked) zones.

### ⚡ **Automation & Networking**

* **Playbook Engine:** Execute batched administrative tasks via JSON scripts.
* **Network Toolkit:** Built-in Port Scanner, Ping utility, and active Connection Ticker.

---

## 🚀 Installation

### Option A: Linux Package (Recommended)

We provide a ready-to-use Debian package. This installs NetMon-AI as a system command and handles API configuration automatically.

1. **Download** the `.deb` file from the [Releases Page](https://www.google.com/search?q=%23).
2. **Install** via terminal:
```bash
sudo dpkg -i netmon-ai_1.0.0_all.deb
sudo apt-get install -f  # Fixes any missing dependencies

```


3. **Configure:** During installation, you will be prompted to enter your **Groq API Key**.
4. **Run:**
```bash
netmon-ai

```



### Option B: Manual / Developer Setup (Windows & Linux)

If you want to modify the code or run it on Windows:

1. **Clone the Repository:**
```bash
git clone https://github.com/YOUR_USERNAME/NetMon-AI.git
cd NetMon-AI

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt
python -m nltk.downloader wordnet

```


3. **Configure API Key:**
Create a `.env` file in the root directory:
```ini
GROQ_API_KEY=gsk_your_actual_api_key_here

```


4. **Run the Shell:**
```bash
python src/shell.py

```


---

## 🎮 Usage Guide

Once inside the `NetMon-AI` shell, you can use **Native Commands** or **AI Prompts**.

### 🤖 AI Commands (`ask`)

* **System Check:** `ask "How is the server health right now?"`
* **Process Management:** `ask "Find and kill the notepad process"` (Triggers Security Gate)
* **File Operations:** `ask "Go to F:\Logs and list all error files"`
* **Network:** `ask "Scan ports on google.com"`

### 🛠 Native Commands

| Command | Description |
| --- | --- |
| `monitor` | Opens the live TUI dashboard. |
| `connections` | Shows active network connections (Packet Ticker). |
| `pslist` | Lists all running processes with PID and Usage. |
| `register <file>` | Registers a file for Integrity Monitoring. |
| `audit` | Checks registered files for tampering. |
| `run-script <file>` | Executes an automation playbook (JSON). |
| `analyze <log>` | Uses AI to analyze a specific log file for errors. |

---

## 🔒 Security Protocol

NetMon-AI implements a strict **Trust-but-Verify** architecture to prevent AI hallucinations from damaging the system.

1. **Green Zone (Auto-Run):** Read-only commands (e.g., "Show CPU", "List files") are executed immediately.
2. **Red Zone (Human-in-the-Loop):** Destructive commands (e.g., "Kill PID 1234", "Add User") trigger a **Safety Gate**:
> `⚠️ SECURITY ALERT: RED RISK ACTION DETECTED`
> `Proposed Action: KILL_PROC on 1234`
> `Do you authorize this system change? (y/N)`


3. **Blacklist:** The AI is hard-coded to **never** touch system critical paths (e.g., `System32`, `/etc/shadow`) regardless of user prompts.

---

## 📂 Project Structure

```text
NetMon-AI/
├── build_package/       # Debian packaging scripts & templates
├── src/
│   ├── ai/              # NLP Logic, Groq Client, Context Injection
│   ├── core/            # Monitoring, Integrity, Automation, Audit Engines
│   ├── utils/           # UI Helpers, Colors
│   └── shell.py         # Main Secure Intent Router
├── build.sh             # Automated Linux Package Builder
└── requirements.txt     # Python Dependencies

```

---


