# 🚀 NetMon-AI v1.0.0 - Initial Release

**Release Date:** February 1, 2026

## ✨ What's New

This is the **first official release** of NetMon-AI - an intelligent system administration platform combining natural language AI with powerful Linux system management tools.

## 🎯 Key Features Included

- **🤖 Intelligent AI Core** - Natural language interface powered by Groq Cloud & Llama 3.3
- **📊 Live TUI Dashboard** - Real-time CPU/Memory/Disk monitoring with Rich library
- **🛡️ Enterprise Security** - Human-in-the-Loop approval gates for critical operations
- **🔐 Immutable Audit Trail** - Complete compliance logging of all AI actions
- **⚡ Advanced Automation** - JSON-based playbook engine for batch operations
- **📋 14+ System Commands** - Native commands for process, service, and network management
- **🔍 File Integrity Monitoring** - SHA-256 based tampering detection
- **🌐 Network Tools** - Port scanning, ping, bandwidth monitoring

## 📦 Package Contents

```
netmon-ai_1.0.0_all.deb (Debian Package)
├── Source Code (Python 3.8+)
├── Build Scripts
├── Documentation (README + LICENSE)
├── Configuration Templates
└── Installation Scripts with debconf prompts
```

## 🚀 Installation

**Quick Start:**
```bash
# Download
wget https://github.com/ASAD2204/NetMon-AI/releases/download/v1.0.0/netmon-ai_1.0.0_all.deb

# Install
sudo dpkg -i netmon-ai_1.0.0_all.deb

# Setup virtual environment and dependencies
python3 -m venv /opt/netmon-ai-venv
source /opt/netmon-ai-venv/bin/activate
git clone https://github.com/ASAD2204/NetMon-AI.git
cd NetMon-AI
pip install -r requirements.txt
python3 -m nltk.downloader wordnet

# Configure API Key
echo -n "gsk_your_groq_api_key" | base64 | sudo tee /etc/netmon-ai/.env.b64
sudo chmod 600 /etc/netmon-ai/.env.b64

# Run
netmon-ai
```

See [README.md](https://github.com/ASAD2204/NetMon-AI/blob/main/Readme.md) for detailed installation options.

## 📚 Example Usage

```bash
# Monitor system metrics
ask "show me the ram usage"
ask "show me the cpu, ram and disk usage"

# Open live dashboard
ask "open dashboard"

# Process management
ask "kill idle python processes"

# File operations
ask "list files in /var/log"

# Network diagnostics
ask "scan ports on google.com"
```

## 🔐 Security Highlights

- **Human-in-the-Loop Gates** - All critical operations require explicit approval
- **Path Whitelisting** - Protected system directories (`/etc/shadow`, `/root`, `System32`, etc.)
- **Input Sanitization** - Command injection prevention with strict validation
- **Base64 API Key Storage** - Secure credential management in production
- **Immutable Audit Logging** - Full compliance trail for security reviews

## ✅ System Requirements

- **OS:** Linux (Debian/Ubuntu preferred)
- **Python:** 3.8 or higher
- **Disk:** ~500MB (with dependencies)
- **Memory:** 256MB minimum
- **Network:** Internet connection for Groq Cloud API
- **Permissions:** Sudo access for system operations

## 🎓 Academic Project

**Author:** Muhammad Asad (BIT22031)  
**Institution:** University of the Punjab, Gujranwala Campus  
**Course:** System and Network Administration (7th Semester)  
**Instructor:** Mr. Moodser Hussain  

## 🙏 Credits

- **AI Engine:** [Groq Cloud](https://groq.com) & [Llama 3.3](https://www.meta.com/research/llama)
- **TUI Framework:** [Rich](https://github.com/Textualize/rich)
- **NLP Toolkit:** [NLTK](https://www.nltk.org/)
- **System Monitoring:** [psutil](https://github.com/giampaolo/psutil)

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](https://github.com/ASAD2204/NetMon-AI/blob/main/LICENSE) for details.

## 🐛 Known Issues / Limitations

- Requires virtual environment setup post-installation (modern Ubuntu limitation)
- API key must be configured manually after Debian package installation
- Tested on Ubuntu 22.04+ and Debian 11+

## 🔗 Documentation

- [Full README](https://github.com/ASAD2204/NetMon-AI/blob/main/Readme.md)
- [Complete Commands Reference](https://github.com/ASAD2204/NetMon-AI#-complete-commands-reference)
- [Architecture & Security Details](https://github.com/ASAD2204/NetMon-AI#-architecture)

## 🚀 Next Steps

- Try out the demo commands above
- Read the full [README](https://github.com/ASAD2204/NetMon-AI/blob/main/Readme.md) for advanced usage
- Report issues or suggest features on the [Issues page](https://github.com/ASAD2204/NetMon-AI/issues)

## 📞 Support

For installation issues or questions, please:
1. Check the [README troubleshooting section](https://github.com/ASAD2204/NetMon-AI#-configuration--setup)
2. Review the [Commands Reference](https://github.com/ASAD2204/NetMon-AI#-complete-commands-reference)
3. Open an [issue](https://github.com/ASAD2204/NetMon-AI/issues) with details

---

**Thank you for trying NetMon-AI! ⭐ Star the repo if you find it useful!**