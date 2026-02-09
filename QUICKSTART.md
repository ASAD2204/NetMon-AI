# 🎯 NetMon-AI Quick Start Guide

## Installation (5 minutes)

### Windows
```powershell
# Clone repository
git clone https://github.com/ASAD2204/NetMon-AI.git
cd NetMon-AI

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pyreadline3  # For Windows tab completion
python -m nltk.downloader wordnet

# Set API key
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run
python src/shell.py
```

### Linux
```bash
# Clone repository
git clone https://github.com/ASAD2204/NetMon-AI.git
cd NetMon-AI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python3 -m nltk.downloader wordnet

# Set API key
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run
python3 src/shell.py
```

## First Time Setup

### 1. Configure Alerts (Optional)
```bash
# View current thresholds
alert-config

# Customize for your needs
set-threshold cpu 70 85
set-threshold memory 75 90
set-threshold disk 80 95
```

### 2. Set Up Aliases
```bash
# Create shortcuts for common tasks
alias ll "ls -la"
alias check "health"
alias backup "export"

# View all aliases
aliases
```

### 3. Check System Health
```bash
# Get overall health score
health

# Output shows:
# - CPU, Memory, Disk usage
# - Individual scores
# - Overall health rating
```

## Essential Commands

### AI Queries
```bash
# Ask anything about your system
ask "show me CPU usage"
ask "what processes are using most memory"
ask "show me network connections"
ask "open the dashboard"
```

### System Monitoring
```bash
monitor              # Live dashboard (Ctrl+C to exit)
health               # System health score
pslist               # List all processes
connections          # Show network connections
```

### File Operations
```bash
ls /var/log          # List directory
cat error.log        # View file contents
search "error" app.log   # Search in file
touch newfile.txt    # Create file
pwd                  # Current directory
cd /tmp              # Change directory
```

### Alerts & Notifications
```bash
alerts               # View recent alerts (last 10)
alerts 20            # View last 20 alerts
alert-config         # Show configuration
```

### User Management
```bash
password-policy      # View password requirements
sessions             # Show active sessions
```

### Security & Integrity
```bash
register /etc/hosts  # Monitor file for changes
audit                # Check all registered files
analyze /var/log/auth.log  # AI-powered log analysis
```

### Automation
```bash
run-script playbook.json   # Execute automation playbook
```

### Utilities
```bash
history              # Show command history
export               # Export system state
help                 # Show all commands
clear                # Clear screen
```

## Advanced Usage

### Piping & Redirection
```bash
# Pipe commands
pslist | search python

# Save output to file
pslist > processes.txt
health > health_report.txt

# Chain multiple commands
cat error.log | search "critical"
```

### Working with Git Projects
```bash
# Navigate to a Git repo
cd /path/to/project

# Prompt automatically shows branch
/path/to/project (main) $

# Your commands here...
```

### Creating Workflows
```bash
# Create a daily health check workflow
alias daily-check "health && alerts 10 && export"

# Run it
daily-check

# Create monitoring aliases
alias cpu-monitor "ask show cpu usage"
alias mem-monitor "ask show memory usage"
alias disk-monitor "ask show disk usage"
```

### Setting Up Alerts

1. **Configure thresholds for your environment:**
   ```bash
   # For development machine (relaxed)
   set-threshold cpu 80 95
   set-threshold memory 85 95
   
   # For production server (strict)
   set-threshold cpu 60 75
   set-threshold memory 70 85
   set-threshold disk 75 90
   ```

2. **Enable email notifications (optional):**
   - Edit `data/alert_config.json`
   - Add SMTP settings
   - Add recipient emails

3. **Test alerts:**
   ```bash
   # Check current metrics
   health
   
   # View recent alerts
   alerts
   ```

## Tips & Tricks

### 1. Use Tab Completion
- Press `Tab` to autocomplete commands and filenames
- Works for built-in commands, aliases, and files

### 2. Search History
- Use `Ctrl+R` (Linux/Mac) to search command history
- Type part of a command to find it

### 3. Create a .netmonrc (Future feature)
Save your favorite aliases and settings

### 4. Monitor Continuously
```bash
# Run dashboard in background terminal
monitor

# Work in another terminal
```

### 5. Regular Health Checks
```bash
# Create a cron job (Linux)
*/15 * * * * /path/to/venv/bin/python /path/to/src/shell.py -c "health && export"
```

## Troubleshooting

### Issue: "Rich library not found"
```bash
pip install rich
```

### Issue: "readline not available" (Windows)
```bash
pip install pyreadline3
```

### Issue: "Permission denied" for user management
```bash
# Run with elevated privileges
sudo python3 src/shell.py  # Linux
# Run as Administrator      # Windows
```

### Issue: API key not working
```bash
# Check .env file
cat .env

# Verify format
GROQ_API_KEY=gsk_your_key_here
```

### Issue: Alerts not showing
```bash
# Check if alerts are enabled
alert-config

# View alert history
alerts 50
```

## Next Steps

1. **Customize Your Setup**
   - Set thresholds for your environment
   - Create useful aliases
   - Configure alert channels

2. **Explore AI Capabilities**
   - Ask complex questions
   - Use natural language
   - Let AI help with diagnostics

3. **Automate Tasks**
   - Create playbooks for routine operations
   - Use aliases for workflows
   - Export system state regularly

4. **Monitor Proactively**
   - Set up alerts
   - Check health regularly
   - Review alert history

## Getting Help

```bash
# Show all commands
help

# Check documentation
cat README.md
cat ENHANCEMENTS.md

# GitHub Issues
https://github.com/ASAD2204/NetMon-AI/issues
```

## Community

- 📖 [Full Documentation](README.md)
- 🚀 [Enhancement Guide](ENHANCEMENTS.md)
- 💬 [GitHub Discussions](https://github.com/ASAD2204/NetMon-AI/discussions)
- 🐛 [Report Issues](https://github.com/ASAD2204/NetMon-AI/issues)

---

**Happy Monitoring! 🎉**
