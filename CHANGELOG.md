# NetMon-AI Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-09

### Added
- **Shell Enhancements**
  - Piping support with `|` operator for chaining commands
  - Output redirection with `>` operator to save command output
  - Git branch detection in command prompt
  - Persistent command history (last 1000 commands)
  - Enhanced tab completion for commands, files, and aliases
  - Ctrl+R reverse search for command history (Unix-like systems)
  - UTF-8 encoding support for Windows

- **Command Aliases System**
  - `alias <name> <command>` - Create command shortcuts
  - `unalias <name>` - Remove aliases
  - `aliases` - List all defined aliases
  - Persistent storage in `data/aliases.json`
  - Auto-expansion of aliases in prompt

- **File Operations**
  - `search <text> <file>` - Grep-like text search in files
  - `cat <file>` - Display file contents
  - `touch <file>` - Create or update files
  - Enhanced `ls` with color-coded output (blue=directories, green=files)
  - `pwd` - Print working directory
  - `cd <dir>` - Change directory with better error handling

- **System Health & Monitoring**
  - `health` - Overall system health score (0-100)
  - Component-level scoring (CPU, Memory, Disk)
  - Status classification (EXCELLENT, GOOD, FAIR, POOR)
  - Automatic integration with alert system

- **Intelligent Alerting System** (New Module: `src/core/alerting.py`)
  - Configurable thresholds per resource (CPU, Memory, Disk)
  - Multi-channel notifications (console, file, email, webhook)
  - Alert suppression/deduplication (5-minute window)
  - Alert history tracking (last 1000 alerts)
  - Severity levels (CRITICAL, WARNING, INFO)
  - `alerts [count]` - View recent alerts
  - `alert-config` - Show alert configuration
  - `set-threshold <resource> <warning> <critical>` - Configure thresholds

- **Enhanced User Management** (Enhanced: `src/core/user_manager.py`)
  - Password strength validation
  - Password complexity requirements (uppercase, lowercase, numbers, special chars)
  - Configurable password policies in `data/password_policies.json`
  - Password expiry tracking (90 days default)
  - Session management and tracking
  - Failed login attempt monitoring
  - `password-policy` - Show password requirements
  - `sessions` - View active user sessions

- **Enhanced Log Viewer** (Enhanced: `src/core/log_viewer.py`)
  - Log file bookmarks for quick access
  - `tail <logfile>` - Follow logs in real-time
  - `log-stats <logfile>` - Generate log statistics
  - `bookmark-log <name> <path>` - Bookmark a log file
  - `bookmarks` - List all log bookmarks
  - Keyword search with match count

- **System State Export**
  - `export` - Export complete system snapshot
  - JSON format with timestamp
  - Includes metrics, processes, aliases, git branch, working directory
  - Saved to `data/system_snapshot_YYYYMMDD_HHMMSS.json`

- **Configuration Files**
  - `data/aliases.json.example` - Example command aliases
  - `data/alert_config.json.example` - Alert configuration template
  - `data/password_policies.json.example` - Password policy template
  - `data/log_bookmarks.json` - Log file bookmarks

- **Documentation**
  - `ENHANCEMENTS.md` - Comprehensive feature documentation
  - `QUICKSTART.md` - 5-minute quick start guide
  - `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
  - `VERSION_COMPARISON.md` - v1.0.0 vs v1.1.0 feature comparison
  - `RELEASE_NOTES_v1.1.0.md` - Full v1.1.0 release notes
  - `CHANGELOG.md` - This file
  - `VERSION` - Version tracking file

- **Testing**
  - `tests/test_enhancements.py` - Comprehensive test suite
  - 7 test categories, 100% pass rate
  - UTF-8 encoding support for Windows testing

### Changed
- Updated `src/shell.py` with 1,500+ lines of new functionality
- Enhanced command routing with new features
- Improved autocomplete with file path completion
- Better error handling throughout
- Updated help system with new commands
- Enhanced welcome banner with feature highlights
- Improved cross-platform compatibility

### Fixed
- UTF-8 encoding issues on Windows
- Readline import errors on Windows (added pyreadline3 fallback)
- Git detection error handling
- Command history persistence
- Path validation for cross-platform compatibility
- Escape sequence warnings in shell

### Security
- Enhanced password validation with configurable policies
- Session tracking for audit purposes
- Alert logging for security events
- Maintained all existing security features:
  - Human-in-the-loop (HITL) approval gates
  - Path whitelisting
  - Input sanitization
  - Command injection prevention
  - Risk classification (GREEN/YELLOW/RED)

### Performance
- Efficient history management (circular buffer)
- Alert suppression prevents flooding
- Cached configuration loading
- Optimized file operations

### Deprecated
- None

### Removed
- None

### Breaking Changes
- None - Full backward compatibility with v1.0.0

## [1.0.0] - 2026-02-01

### Added
- Initial release
- AI-powered natural language interface with Groq Cloud
- Real-time system monitoring dashboard
- Process management (list, kill)
- Network tools (ping, port scan, bandwidth, connections)
- File integrity monitoring (FIM)
- Service management
- User management
- Log analysis with AI
- Automation playbook engine
- Human-in-the-loop (HITL) security protocol
- Immutable audit trail
- Risk classification system
- Path whitelisting and input sanitization
- Base64 API key storage
- Debian package with debconf integration
- Cross-platform support (Windows/Linux)
- Rich TUI dashboard
- Command history (basic)
- Help system
- Safe native command execution

### Security
- Human-in-the-loop approval for critical operations
- Path whitelisting (forbidden paths)
- Input sanitization
- Command injection prevention
- Risk-based classification (GREEN, YELLOW, RED)
- Audit logging for all actions
- Secure API key storage

---

## Version History Summary

| Version | Date | Type | Changes |
|---------|------|------|---------|
| 1.1.0 | 2026-02-09 | Major | +30 features, +17 commands, enhanced UX |
| 1.0.0 | 2026-02-01 | Initial | First public release |

---

## Upgrade Guide

### From v1.0.0 to v1.1.0

**Good news:** No breaking changes! All v1.0.0 functionality works identically in v1.1.0.

#### Steps:
1. **Backup your data:**
   ```bash
   export  # If you have v1.1.0 already
   # Or manually backup data/ folder
   ```

2. **Update code:**
   ```bash
   git pull origin main
   # Or download v1.1.0 release
   ```

3. **Install any new dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure new features (optional):**
   ```bash
   # Set up alerts
   set-threshold cpu 75 90
   
   # Create aliases
   alias ll "ls -la"
   
   # View password policies
   password-policy
   ```

5. **Test:**
   ```bash
   python tests/test_enhancements.py
   ```

---

## Contributing

We welcome contributions! Please see our contribution guidelines.

## Support

- **Documentation:** See [QUICKSTART.md](QUICKSTART.md) for getting started
- **Issues:** https://github.com/ASAD2204/NetMon-AI/issues
- **Email:** asadrafaqt16@gmail.com

---

**Stay updated:** Watch this repository for future releases!
