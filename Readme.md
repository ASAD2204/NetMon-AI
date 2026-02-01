# 🌐 NetMon-AI: Intelligent Network Monitoring Platform

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Groq Cloud](https://img.shields.io/badge/Powered%20by-Groq%20Cloud-brightgreen.svg)](https://groq.com)
[![Llama 3.3](https://img.shields.io/badge/LLM-Llama%203.3-orange.svg)](https://www.meta.com/research/llama)

> **"Talk to your server."**  
> Transform complex system administration into simple, natural language conversations.  
> Powered by **Groq Cloud** and **Llama 3.3**, combining CLI power with AI intelligence.

[Features](#-key-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Security](#-security-protocol)

</div>

---

## 📖 Overview

**NetMon-AI** is a next-generation intelligent system administration platform that bridges the gap between manual command-line operations and intelligent automation. It provides a unified, conversational shell interface where sysadmins can:

- 🔍 **Monitor** system health in real-time with live TUI dashboards
- 🤖 **Interact** using natural language (no syntax memorization required)
- 🛡️ **Manage** processes, services, and network configurations safely
- 📊 **Automate** complex administrative tasks via JSON playbooks
- 🔐 **Audit** system changes and maintain compliance logs
- ✅ **Verify** AI decisions through human-in-the-loop security gates

Unlike traditional CLI tools, NetMon-AI features a **Human-in-the-Loop (HITL) Security Protocol**, ensuring that AI suggestions for critical operations (killing processes, modifying configs, deleting files) require explicit administrator approval before execution.

---

## ✨ Key Features

### 🧠 **Intelligent AI Core**
- **Natural Language Processing:** Ask questions like *"Why is CPU usage high?"*, *"Kill idle Python processes"*, or *"Show me recent login failures"*
- **Context-Aware:** AI understands your current directory, OS, system metrics, and security context
- **Synonym Resolver:** Accepts variations like "terminate", "stop", "kill", "nuke" → unified intent
- **Robust Fallbacks:** Handles malformed AI responses gracefully with rule-based heuristics
- **JSON Intent Extraction:** Extracts structured actions from LLM output with validation

### 📊 **Real-Time System Dashboard**
- **Live TUI:** Professional, responsive terminal UI using `Rich` library
- **Multi-Metric Display:** CPU, Memory, Disk, and Network usage in one view
- **Color-Coded Alerts:** GREEN (healthy) → YELLOW (warning) → RED (critical)
- **Live Updates:** Refresh rates configurable, suitable for large monitors or scripts
- **Compact Mode:** Query individual metrics: `ask "show me the ram usage"` → single-line response

### 🛡️ **Enterprise-Grade Security**
- **File Integrity Monitoring (FIM):** SHA-256 hashing for critical file change detection
- **Immutable Audit Trail:** Every AI action (approved/rejected) logged to `data/ai_audit.log`
- **Risk Classification:** GREEN (safe read-only) / YELLOW (non-destructive) / RED (critical)
- **Path Whitelisting:** Hard-coded restrictions on system directories (e.g., `/etc/shadow`, `System32`)
- **Input Sanitization:** Command injection prevention via strict path validation and pattern matching
- **Base64 API Key Storage:** Production API keys encrypted in `/etc/netmon-ai/.env.b64`

### ⚡ **Automation & Networking**
- **Playbook Engine:** Execute batched administrative tasks from JSON files
- **Network Toolkit:** Port scanning, ping, bandwidth monitoring, active connection tracking
- **Service Management:** Start, stop, restart system services via AI or CLI
- **User Management:** Add/remove users and manage permissions (with security approval)
- **Process Management:** List, monitor, and terminate processes with resource metrics

### 📝 **Compliance & Monitoring**
- **Structured Logging:** All events recorded with timestamps and user context
- **Persistent History:** Command history stored in `data/command_history.json`
- **Analysis Cache:** AI analysis results cached for performance optimization
- **Multi-Platform:** Windows and Linux support (with platform-specific adaptations)

---

## 🚀 Installation

### Option A: Linux Debian Package (Recommended)

#### Method 1: Build the Package Yourself

1. **Clone the Repository:**
```bash
git clone https://github.com/YOUR_USERNAME/NetMon-AI.git
cd NetMon-AI

```

2. **Build the Debian Package:**
```bash
chmod +x build.sh
./build.sh

```
This creates `netmon-ai_1.0.0_all.deb` in your current directory.

3. **Install the Package:**
```bash
sudo dpkg -i netmon-ai_1.0.0_all.deb
sudo apt-get install -f  # Fix any missing dependencies

```

#### Method 2: Download Pre-Built Package (When Available)

When releases are published to GitHub:
```bash
# Download from GitHub Releases page
cd /tmp
wget https://github.com/YOUR_USERNAME/NetMon-AI/releases/download/v1.0.0/netmon-ai_1.0.0_all.deb

# Install
sudo dpkg -i netmon-ai_1.0.0_all.deb
sudo apt-get install -f

```

---

**API Key Configuration:**
   - You'll be prompted during installation to enter your Groq API Key via `debconf`
   - Key is stored securely: `/etc/netmon-ai/.env.b64` (base64-encoded, permissions: 600)

3. **Install Python Dependencies (Post-Install):**

   **Option A1: Virtual Environment (Recommended):**
   ```bash
   # Create virtual environment
   python3 -m venv /opt/netmon-ai-venv
   
   # Activate it
   source /opt/netmon-ai-venv/bin/activate
   
   # Clone repo to access requirements.txt (or copy it manually)
   git clone https://github.com/YOUR_USERNAME/NetMon-AI.git
   cd NetMon-AI
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Download NLTK data
   python3 -m nltk.downloader wordnet
   
   # Test the installation
   ask "show me the ram usage"
   ```
   
   **To run NetMon-AI in future sessions:**
   ```bash
   source /opt/netmon-ai-venv/bin/activate
   netmon-ai
   ```

   **Option A2: System-Wide (Not Recommended on Modern Ubuntu):**
   
   Modern Ubuntu/Debian systems restrict `sudo pip3 install` to prevent breaking system Python. Use **Option A1 (Virtual Environment)** instead for better compatibility.

### Option B: Development Setup (Windows / Linux)

1. **Clone Repository:**
```bash
git clone https://github.com/YOUR_USERNAME/NetMon-AI.git
cd NetMon-AI

```

2. **Create Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
python -m nltk.downloader wordnet

```

4. **Configure API Key:**
```bash
# Create .env file in project root
echo "GROQ_API_KEY=gsk_your_api_key_here" > .env

# Enable local .env loading (dev only):
# Edit src/ai/groq_client.py and change: LOAD_ENV = True
```

5. **Run:**
```bash
python src/shell.py

```

---

## 🎮 Quick Start

### Start the Shell
```bash
netmon-ai
```

### Example Queries
```bash
ask "show me the ram usage"
ask "show me the cpu, ram and disk usage"
ask "open dashboard"
ask "kill process python"
ask "list files in /var/log"
ask "go to /tmp and list files"
```

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                       NetMon-AI Shell                           │
│  (Interactive CLI with command routing & intent execution)      │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼────┐           ┌───────▼──────┐
   │ Native  │           │  AI Intent   │
   │Commands │           │   Router     │
   └────┬────┘           └───────┬──────┘
        │                        │
        │         ┌──────────────┼──────────────┐
        │         │              │              │
   ┌────▼──┐  ┌──▼────┐  ┌──────▼──┐  ┌──────▼───┐
   │ Core  │  │ NLP   │  │Security │  │ Audit    │
   │Module │  │Engine │  │ Gates   │  │Logger    │
   └────┬──┘  └──┬────┘  └──┬──────┘  └──────────┘
        │        │          │
        └────────┼──────────┘
                 │
            ┌────▼────────────────────┐
            │  Groq Cloud API (Llama) │
            └─────────────────────────┘
```

### Project Structure

```
NetMon-AI/
├── 📄 build.sh                          # Debian package build script
├── 📄 Readme.md                         # Documentation
├── 📄 LICENSE                           # MIT License
├── 📄 requirements.txt                  # Python dependencies
│
├── 📁 build_package/                    # Debian packaging
│   └── DEBIAN/
│       ├── control                      # Package metadata
│       ├── config                       # Debconf prompts
│       ├── templates                    # Debconf templates
│       └── postinst                     # Post-install script
│
├── 📁 src/                              # Main application source
│   ├── 📄 shell.py                      # Main CLI shell & command router
│   │
│   ├── 📁 ai/                           # AI & NLP components
│   │   ├── groq_client.py               # Groq API client wrapper
│   │   ├── nlp_interface.py             # Intent extraction & routing
│   │   ├── nlp_utils.py                 # Synonym resolver & normalization
│   │   ├── log_analyzer.py              # AI-powered log analysis
│   │   └── __pycache__/
│   │
│   ├── 📁 core/                         # Core system modules
│   │   ├── monitoring.py                # Live system metrics (CPU/MEM/DISK)
│   │   ├── process_manager.py           # Process listing & termination
│   │   ├── service_manager.py           # Service lifecycle management
│   │   ├── network_tools.py             # Networking utilities (ping, scan, etc.)
│   │   ├── user_manager.py              # User & permission management
│   │   ├── log_viewer.py                # Log file viewing & parsing
│   │   ├── integrity.py                 # File Integrity Monitoring (FIM)
│   │   ├── auditor.py                   # Audit logging & compliance
│   │   ├── automation.py                # Playbook engine
│   │   └── __pycache__/
│   │
│   ├── 📁 utils/                        # Utility modules
│   │   ├── colors.py                    # ANSI color formatting
│   │   ├── helpers.py                   # Common helper functions
│   │   └── __pycache__/
│   │
│   └── 📁 data/                         # Runtime data (created at first run)
│       ├── analysis_cache.json          # Cached AI analyses
│       ├── command_history.json         # Command history log
│       └── ai_audit.log                 # Comprehensive audit trail
│
└── 📁 __pycache__/                      # Python cache (ignored)
```

### Module Responsibilities

| Module | Purpose | Key Classes/Functions |
|--------|---------|----------------------|
| **shell.py** | Main CLI interface, command routing, intent execution | NetMonShell, route_ai_intent(), _sanitize_and_validate_path() |
| **groq_client.py** | LLM API communication, prompt engineering | GroqAIClient, call_groq_api(), find_env() |
| **nlp_interface.py** | Intent extraction, validation, fallback heuristics | NLPInterface, process_query(), extract_first_json(), _validate_intent() |
| **monitoring.py** | System metrics collection & live dashboard | SystemMonitor, get_metrics(), display_dashboard() |
| **process_manager.py** | Process enumeration, filtering, termination | ProcessManager, list_processes(), kill_process() |
| **service_manager.py** | Service control (start/stop/restart) | ServiceManager, start_service(), stop_service() |
| **auditor.py** | Compliance logging of all AI actions | AuditLogger, log_action() |
| **integrity.py** | File hash tracking & tamper detection | IntegrityMonitor, register_file(), verify_integrity() |
| **automation.py** | Playbook execution engine | PlaybookEngine, execute_playbook() |
| **network_tools.py** | Network diagnostics and scanning | NetworkTools, ping(), port_scan(), get_connections() |

---

## 🔐 Security Protocol

NetMon-AI implements a **Trust-but-Verify** security model to prevent AI hallucinations from damaging systems.

### Risk Classification

```
GREEN (Read-Only)  ✅ Auto-Execute
  ├─ Monitor CPU/Memory/Disk
  ├─ List files/processes
  ├─ Show network connections
  └─ View logs

YELLOW (Non-Destructive)  ⚠️ Confirm Required
  ├─ Restart services
  ├─ Change directories
  └─ Install packages

RED (Critical/Destructive)  🛑 Security Gate
  ├─ Kill processes
  ├─ Delete files
  ├─ Add/remove users
  ├─ Modify system configs
  └─ Network operations
```

### Security Features

1. **Input Validation:**
   - Regex-based injection prevention
   - Suspicious pattern detection (`;`, `|`, `&&`, backticks, `$()`)
   - Path normalization & whitelist enforcement

2. **Path Protection:**
   - Hard-coded forbidden paths: `/etc/shadow`, `/root`, `System32`, etc.
   - Case-insensitive matching on Windows
   - Directory traversal (`../../../`) blocked

3. **Audit Trail:**
   - Every action (approved/rejected) logged with timestamp
   - User context and original query preserved
   - Full compliance history for security reviews

4. **API Key Security:**
   - Development: Plain `.env` (debug only, excluded from git)
   - Production: Base64-encoded storage at `/etc/netmon-ai/.env.b64`
   - Permissions: `600` (readable only by owner)

---

## ⚙️ Configuration & Setup

### Getting Your Groq API Key

1. Visit [Groq Console](https://console.groq.com/keys)
2. Sign up for a free account (if needed)
3. Generate a new API key
4. Copy the key (starts with `gsk_`)

### Setting Up API Key After Installation

**For Linux Debian Package Installation:**
```bash
# Encode your API key in base64
echo -n "gsk_your_actual_key_here" | base64 | sudo tee /etc/netmon-ai/.env.b64

# Set correct permissions
sudo chmod 600 /etc/netmon-ai/.env.b64

# Verify it's set
cat /etc/netmon-ai/.env.b64
```

**For Development (Local Testing):**
```bash
# Create .env file in project root
echo "GROQ_API_KEY=gsk_your_actual_key_here" > .env

# Enable local .env loading
# Edit src/ai/groq_client.py and change line 6:
# LOAD_ENV = False  →  LOAD_ENV = True

# Then test
python src/shell.py
```

### Verifying Installation

Test that everything works:
```bash
# Activate venv if using one
source /opt/netmon-ai-venv/bin/activate

# Test a simple query
ask "show me the ram usage"

# Or test the full dashboard
ask "open dashboard"
```

If you see system metrics, your installation is successful! ✅

---

## 📊 Performance & Metrics

| Metric | Specification | Notes |
|--------|--------------|-------|
| **Dashboard Refresh Rate** | 2 Hz (0.5s) | Configurable in code |
| **API Response Time** | <5s avg | Groq Cloud latency |
| **Memory Footprint** | ~80-150 MB | With venv & dependencies |
| **Supported Processes** | Unlimited | Limited by system resources |
| **Audit Log Retention** | Unlimited | Manual cleanup recommended |
| **Cache TTL** | 5 minutes | Analysis cache expiration |

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Docker containerization
- [ ] REST API wrapper
- [ ] Web dashboard frontend
- [ ] Additional LLM providers (OpenAI, Claude, Ollama)
- [ ] Enhanced logging & visualization
- [ ] Unit tests & integration tests (currently ~15% coverage)
- [ ] Advanced playbook templating
- [ ] Distributed monitoring for multiple hosts

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🎓 Academic Project

**NetMon-AI** is a 7th semester System and Network Administration course project.

**Author:** Muhammad Asad  
**Roll No:** BIT22031  
**Degree:** B.S. (Hons) Information Technology  
**University:** University of the Punjab, Gujranwala Campus  
**Department:** Department of Information Technology  
**Course Instructor:** Mr. Moodser Hussain  

---

## 🎓 Credits & Acknowledgments

- **AI Engine:** [Groq Cloud](https://groq.com) & [Llama 3.3](https://www.meta.com/research/llama)
- **TUI Framework:** [Rich](https://github.com/Textualize/rich) by Will McGugan
- **NLP Toolkit:** [NLTK](https://www.nltk.org/)
- **System Monitoring:** [psutil](https://github.com/giampaolo/psutil)
- **Debian Packaging:** [Debconf](https://wiki.debian.org/Debconf)

---

## 🚧 Roadmap

**v1.1** (Q1 2026)
- Web-based dashboard (Flask + React)
- REST API for remote management
- Docker & Kubernetes integration

**v1.2** (Q2 2026)
- Multi-host distributed monitoring
- Advanced analytics & trend analysis
- Integration with enterprise SIEM systems

**v2.0** (Q3 2026)
- Support for additional LLM providers
- Advanced threat detection
- Compliance reporting (ISO 27001, SOC 2)

---

<div align="center">

**Made with ❤️ for system administrators and DevOps engineers**

⭐ If this project helped you, please give it a star!

[Report Bug](https://github.com/ASAD2204/NetMon-AI/issues) • [Request Feature](https://github.com/ASAD2204/NetMon-AI/issues)

</div>