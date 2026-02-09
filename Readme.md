# 🌐 NetMon-AI: Intelligent Network Monitoring Platform

<div align="center">

[![Version](https://img.shields.io/badge/Version-1.1.0-blue.svg)](https://github.com/ASAD2204/NetMon-AI/releases)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Groq Cloud](https://img.shields.io/badge/Powered%20by-Groq%20Cloud-brightgreen.svg)](https://groq.com)
[![Llama 3.3](https://img.shields.io/badge/LLM-Llama%203.3-orange.svg)](https://www.meta.com/research/llama)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

> **"Talk to your server."**  
> Transform complex system administration into simple, natural language conversations.  
> Powered by **Groq Cloud** and **Llama 3.3**, combining CLI power with AI intelligence.

[Features](#-key-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [What's New](#-whats-new-in-v110) • [Documentation](#-documentation)

</div>

---

## 🎉 What's New in v1.1.0

**Major Feature Release** (February 9, 2026) - [Full Release Notes](RELEASE_NOTES_v1.1.0.md)

- ✨ **Enhanced Shell:** Piping (`|`), redirection (`>`), Git branch detection
- 🔔 **Intelligent Alerts:** Configurable thresholds, multi-channel notifications
- 🔗 **Command Aliases:** Create shortcuts for frequent tasks
- 📊 **Health Scoring:** Overall system health rating (0-100)
- 👥 **Password Policies:** Strength validation, expiry tracking
- 📁 **Advanced File Ops:** `search`, `cat`, `touch` commands
- 💾 **System Export:** Complete state snapshots
- 📋 **Enhanced Logs:** Bookmarks, statistics, real-time tailing

**[View Full Changelog](VERSION_COMPARISON.md)** | **[Quick Start Guide](QUICKSTART.md)**

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

### � **Enhanced Shell Experience** (v1.1.0)
- **Piping & Redirection:** Use `|` and `>` operators like a native shell
- **Git Branch Detection:** Shows current branch in prompt automatically
- **Command Aliases:** Create shortcuts for frequently used commands
- **Persistent History:** Commands saved across sessions with Ctrl+R search
- **Smart Autocomplete:** Tab completion for commands, files, and aliases
- **Advanced File Ops:** `search`, `cat`, `touch` commands built-in

### 📊 **Real-Time System Dashboard**
- **Live TUI:** Professional, responsive terminal UI using `Rich` library
- **Multi-Metric Display:** CPU, Memory, Disk, and Network usage in one view
- **Color-Coded Alerts:** GREEN (healthy) → YELLOW (warning) → RED (critical)
- **System Health Score:** Overall health rating (0-100) with status
- **Live Updates:** Refresh rates configurable, suitable for large monitors or scripts
- **Compact Mode:** Query individual metrics: `ask "show me the ram usage"` → single-line response

### 🔔 **Intelligent Alerting System** (v1.1.0)
- **Multi-Channel Notifications:** Console, file, email, and webhook support
- **Configurable Thresholds:** Per-resource warning and critical levels
- **Alert Suppression:** Automatic deduplication (5-minute window)
- **Alert History:** Track and review past alerts
- **Real-Time Monitoring:** Automatic alert triggering on threshold breach

### 🛡️ **Enterprise-Grade Security**
- **File Integrity Monitoring (FIM):** SHA-256 hashing for critical file change detection
- **Immutable Audit Trail:** Every AI action (approved/rejected) logged to `data/ai_audit.log`
- **Risk Classification:** GREEN (safe read-only) / YELLOW (non-destructive) / RED (critical)
- **Path Whitelisting:** Hard-coded restrictions on system directories (e.g., `/etc/shadow`, `System32`)
- **Input Sanitization:** Command injection prevention via strict path validation and pattern matching
- **Base64 API Key Storage:** Production API keys encrypted in `/etc/netmon-ai/.env.b64`
- **Password Policies:** Enforce complexity, expiry, and strength requirements
- **Session Management:** Track active sessions and login attempts

### ⚡ **Automation & Networking**
- **Playbook Engine:** Execute batched administrative tasks from JSON files
- **Network Toolkit:** Port scanning, ping, bandwidth monitoring, active connection tracking
- **Service Management:** Start, stop, restart system services via AI or CLI
- **User Management:** Add/remove users with password validation and manage permissions
- **Process Management:** List, monitor, and terminate processes with resource metrics
- **System State Export:** Backup complete system configuration and metrics

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
git clone https://github.com/ASAD2204/NetMon-AI.git
cd NetMon-AI

```

2. **Build the Debian Package:**
```bash
chmod +x build.sh
./build.sh

```
This creates `netmon-ai_1.1.0_all.deb` in your current directory.

3. **Install the Package:**
```bash
sudo dpkg -i netmon-ai_1.1.0_all.deb

```

#### Method 2: Download Pre-Built Package (When Available)

When releases are published to GitHub:
```bash
# Download from GitHub Releases page
cd /tmp
wget https://github.com/ASAD2204/NetMon-AI/releases/download/v1.1.0/netmon-ai_1.1.0_all.deb

# Install
sudo dpkg -i netmon-ai_1.1.0_all.deb

```

4. **Post-Installation Setup:**

#### Option 1: Run from Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd ~/NetMon-AI

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python3 -m nltk.downloader wordnet

# Create .env file with your Groq API key
echo "GROQ_API_KEY=your_api_key_here" > .env
chmod 600 .env

# Fix file permissions (if cloned/built with sudo)
sudo chown -R $USER:$USER ~/NetMon-AI

# Create data directory
mkdir -p ~/NetMon-AI/data

# Run the application
python3 src/shell.py
```

**Create an alias for easy access:**
```bash
echo 'alias netmon="cd ~/NetMon-AI && source venv/bin/activate && python3 src/shell.py"' >> ~/.bashrc
source ~/.bashrc

# Now you can run:
netmon
```

#### Option 2: Run Installed Package with System-Wide Dependencies

```bash
# Install dependencies with environment variable approach
sudo pip3 install --break-system-packages groq rich psutil nltk python-dotenv
python3 -m nltk.downloader wordnet

# Set API key as environment variable
echo 'export GROQ_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc

# Run the installed package
netmon-ai
```

**API Key Configuration Options:**

1. **Environment Variable (Simplest):**
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```

2. **Project .env File (Development):**
   ```bash
   echo "GROQ_API_KEY=your_api_key_here" > ~/NetMon-AI/.env
   chmod 600 ~/NetMon-AI/.env
   ```

3. **System-Wide .env (Production):**
   ```bash
   echo "GROQ_API_KEY=your_api_key_here" | sudo tee /usr/share/netmon-ai/.env
   sudo chmod 600 /usr/share/netmon-ai/.env
   ```

4. **Base64 Encoded (Production - Most Secure):**
   ```bash
   echo -n "your_api_key_here" | base64 | sudo tee /etc/netmon-ai/.env.b64
   sudo chmod 600 /etc/netmon-ai/.env.b64
   ```

### Option B: Development Setup (Windows / Linux)

1. **Clone Repository:**
```bash
git clone https://github.com/ASAD2204/NetMon-AI.git
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
chmod 600 .env

# NOTE: .env loading is enabled by default in v1.1.0
# The application will automatically find and load your .env file
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

### Example AI Queries

```bash
ask "show me the ram usage"
ask "show me the cpu, ram and disk usage"
ask "open dashboard"
ask "kill process python"
ask "list files in /var/log"
ask "go to /tmp and list files"
ask "why is cpu usage high?"
ask "show me the top 5 memory consuming processes"
```

---

## � Troubleshooting

### Common Issues & Solutions

#### 1. ModuleNotFoundError: No module named 'groq'

**Problem:** Python dependencies not installed for the running environment.

**Solution:**
```bash
# If running from virtual environment
cd ~/NetMon-AI
source venv/bin/activate
pip install -r requirements.txt

# If running installed package system-wide
sudo pip3 install --break-system-packages groq rich psutil nltk python-dotenv
```

#### 2. API Key Not Found / Groq Client Not Initialized

**Problem:** `GROQ_API_KEY` environment variable not set or `.env` file missing.

**Solutions:**

**Option A - Create .env file:**
```bash
cd ~/NetMon-AI
echo "GROQ_API_KEY=your_api_key_here" > .env
chmod 600 .env
```

**Option B - Set environment variable:**
```bash
export GROQ_API_KEY="your_api_key_here"
# Add to ~/.bashrc for persistence
echo 'export GROQ_API_KEY="your_api_key_here"' >> ~/.bashrc
```

#### 3. Permission Denied: '/home/user/NetMon-AI/data/ai_audit.log'

**Problem:** Data directory doesn't exist or has wrong permissions.

**Solution:**
```bash
mkdir -p ~/NetMon-AI/data
sudo chown -R $USER:$USER ~/NetMon-AI
chmod 755 ~/NetMon-AI/data
```

#### 4. Git Pull Conflicts After Update

**Problem:** Local changes conflict with repository updates.

**Solution:**
```bash
cd ~/NetMon-AI

# Fix file permissions (if files owned by root)
sudo chown -R $USER:$USER ~/NetMon-AI

# Discard local changes and get clean update
git reset --hard HEAD
git clean -fd
git pull origin main
```

#### 5. Warning: Error reading encrypted API key: Permission denied

**Problem:** This warning is **harmless** - it's the production key file that doesn't exist in development.

**Explanation:** The system tries 3 methods to load API key:
1. Production: `/etc/netmon-ai/.env.b64` (shows warning if missing)
2. Development: Project `.env` file (✅ works)
3. Environment: `$GROQ_API_KEY` variable

**To suppress the warning (optional):**
```bash
# Create production key file
echo -n \"your_api_key_here\" | base64 | sudo tee /etc/netmon-ai/.env.b64
sudo chmod 600 /etc/netmon-ai/.env.b64
```

#### 6. Debian Package Installation Fails

**Problem:** Dependency conflicts or typing-extensions issues.

**Solution:**
```bash
# Use virtual environment approach instead (recommended)
cd ~/NetMon-AI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/shell.py
```

### Getting Help

- 📖 **Full Documentation:** See [ENHANCEMENTS.md](ENHANCEMENTS.md) and [QUICKSTART.md](QUICKSTART.md)
- 🐛 **Report Issues:** [GitHub Issues](https://github.com/ASAD2204/NetMon-AI/issues)
- 💬 **Ask Questions:** Use `help` command within the shell

---

## �📋 Complete Commands Reference

### Native Commands (Type directly in shell)

| Command | Syntax | Effect | Risk Level |
|---------|--------|--------|-----------|
| **monitor** | `monitor` | Opens live TUI dashboard with CPU/MEM/DISK metrics (2Hz refresh) | 🟢 GREEN |
| **pslist** | `pslist [filter]` | Lists all running processes with PID, CPU%, Memory%, Status | 🟢 GREEN |
| **pskill** | `pskill <pid>` | Terminates a process by PID (requires confirmation) | 🔴 RED |
| **connections** | `connections` | Shows all active network connections (IP, Port, Status) | 🟢 GREEN |
| **register** | `register <file_path>` | Registers a file for Integrity Monitoring (FIM) | 🟡 YELLOW |
| **audit** | `audit` | Checks all registered files for tampering (SHA-256 hash verification) | 🟢 GREEN |
| **analyze** | `analyze <log_file>` | Uses AI to analyze log files for errors/warnings | 🟢 GREEN |
| **service** | `service <name> <action>` | Start/stop/restart system services (e.g., `service nginx start`) | 🔴 RED |
| **network** | `network [scan\|ping\|info]` | Network diagnostics (port scan, ping, connection info) | 🟡 YELLOW |
| **user** | `user <action> [username]` | Add/remove/list users (e.g., `user add john`) | 🔴 RED |
| **run-script** | `run-script <playbook.json>` | Execute JSON automation playbook | 🔴 RED |
| **help** | `help [command]` | Shows available commands or detailed help for specific command | 🟢 GREEN |
| **clear** | `clear` | Clears screen | 🟢 GREEN |
| **exit** | `exit` | Closes NetMon-AI shell | 🟢 GREEN |

### AI Commands (Natural Language via `ask`)

| Query Type | Examples | Effect | Risk Level |
|-----------|----------|--------|-----------|
| **Monitoring** | `ask "show me the ram usage"`, `ask "cpu usage?"` | Returns single metric in compact format | 🟢 GREEN |
| **Dashboard** | `ask "open dashboard"`, `ask "show me the dashboard"` | Opens full live TUI with all metrics | 🟢 GREEN |
| **Process Management** | `ask "kill idle python"`, `ask "terminate chrome"` | Kills specified process (requires confirmation) | 🔴 RED |
| **File Operations** | `ask "list files in /tmp"`, `ask "go to /var/log"` | Lists files in specified directory | 🟡 YELLOW |
| **Network Analysis** | `ask "scan ports on google.com"`, `ask "ping 8.8.8.8"` | Network diagnostics | 🟡 YELLOW |
| **System Analysis** | `ask "why is the system slow?"`, `ask "analyze my logs"` | AI-powered system analysis | 🟢 GREEN |
| **General Q&A** | `ask "what processes are running?"`, `ask "show connections"` | Natural language system queries | 🟢 GREEN |

### Risk Levels Explained

🟢 **GREEN (Read-Only)** - Auto-executed, no confirmation needed
- Safe for automated tasks
- No system state changes

🟡 **YELLOW (Non-Destructive)** - May require confirmation
- System modifications that can be reversed
- Configuration changes

🔴 **RED (Critical/Destructive)** - Requires explicit human approval
- Process termination
- User management
- File deletion
- System configuration changes
- **Security Gate activated**: `⚠️ SECURITY ALERT: RED RISK ACTION DETECTED`

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

## 📚 Documentation

- **[README.md](Readme.md)** - Complete project documentation (this file)
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start guide
- **[ENHANCEMENTS.md](ENHANCEMENTS.md)** - Comprehensive feature guide
- **[VERSION_COMPARISON.md](VERSION_COMPARISON.md)** - v1.0.0 vs v1.1.0 comparison
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation
- **[RELEASE_NOTES_v1.1.0.md](RELEASE_NOTES_v1.1.0.md)** - Full v1.1.0 release notes
- **[RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md)** - Initial release notes

---

## 🎓 Credits & Acknowledgments

- **AI Engine:** [Groq Cloud](https://groq.com) & [Llama 3.3](https://www.meta.com/research/llama)
- **TUI Framework:** [Rich](https://github.com/Textualize/rich) by Will McGugan
- **NLP Toolkit:** [NLTK](https://www.nltk.org/)
- **System Monitoring:** [psutil](https://github.com/giampaolo/psutil)
- **Debian Packaging:** [Debconf](https://wiki.debian.org/Debconf)

**Special Thanks:**
- PyShell project for shell inspiration
- Modern shell experiences (zsh, fish, PowerShell)
- Enterprise monitoring tools (Nagios, Zabbix, Prometheus)

---

## 🚧 Roadmap

**v1.2** (Q2 2026)
- Web-based dashboard (Flask + React)
- REST API for remote management
- Database integration (PostgreSQL/SQLite)

**v1.3** (Q3 2026)
- Docker & Kubernetes integration
- Multi-host distributed monitoring
- Predictive analytics with ML
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