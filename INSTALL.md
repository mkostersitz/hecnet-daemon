# HECNET Daemon Installation Guide

## Prerequisites

- Linux, macOS, or Windows operating system
- Python 3.6 or higher
- **PyDECNET installed and configured** - See [PyDECNET Installation Guide](https://github.com/pkoning2/pydecnet/blob/main/pydecnet/doc/install.txt)
- sudo privileges (for process management and socket cleanup on Linux/macOS)
- Gmail account with app password for email notifications

## PyDECNET Installation

Before setting up the HECNET daemon, you must have PyDECNET installed and configured on your system. PyDECNET is the core DECNET implementation that this daemon monitors and manages.

### Installation Options

1. **Follow the Official Installation Guide**: [PyDECNET Installation Documentation](https://github.com/pkoning2/pydecnet/blob/main/pydecnet/doc/install.txt)

2. **Quick Installation Summary**:
   ```bash
   # Clone PyDECNET repository
   git clone https://github.com/pkoning2/pydecnet.git
   
   # Install PyDECNET (follow the detailed instructions in the link above)
   cd pydecnet
   # ... follow installation steps from official documentation
   ```

3. **Verify Installation**:
   ```bash
   # PyDECNET should be accessible via command line
   which pydecnet
   # or
   pydecnet --help
   ```

**Note**: The HECNET daemon will automatically detect your PyDECNET installation location during setup, whether it's installed system-wide or in a custom location.

## HECNET Daemon Installation

### 1. Clone or Download the Project

```bash
cd ~  # or your preferred directory
git clone https://github.com/mkostersitz/hecnet-daemon.git
cd hecnet-daemon
```

### 2. Create a Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Verify you're in the virtual environment
which python  # Should show path to venv/bin/python (Linux/macOS)
where python   # Should show path to venv\Scripts\python.exe (Windows)
```

### 3. Install Required Packages

```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt

# Verify installation
pip list
```

### 4. Configuration

The HECNET daemon uses a template-based configuration system that keeps your personal settings secure while providing easy setup for new users.

#### Configuration Files

- **`pyvenv.cfg.template`**: Template file (safe to commit to Git)
- **`pyvenv.cfg`**: Your personal configuration (ignored by Git)

The setup script automatically creates `pyvenv.cfg` from the template if it doesn't exist.

#### Automatic Path Detection

The daemon automatically configures the following paths:

- **PyDECNET Binary**: Automatically discovered using system commands (`which`/`where`)
- **Configuration Files**: `./config/` directory in the project
- **Log Files**: `./hecnet/logs/` directory in the project
- **Node Names**: `~/.local/bin/nodenames.conf` (created by decnet-name-update.py)

#### Configure Settings with Setup Script

Run the setup script to configure email settings and target host:

```bash
python setup.py
```

This will interactively configure:
- Email settings (sender, receiver, Gmail app password)
- Target DECNET host to monitor (default: MIM)
- **Automatic name updates** (default: every 48 hours, configurable)
- PyDECNET binary location (auto-discovered)
- Automatically test email configuration

#### Example Setup Session

```
HECNET Daemon Setup Script
========================================
Working directory: /home/user/hecnet-daemon
Configuration file: /home/user/hecnet-daemon/pyvenv.cfg

=== Email Configuration ===
Enter sender email address: your-email@gmail.com
Enter Gmail app password: ****************
Enter receiver email address: alerts@example.com

=== DECNET Configuration ===
Enter DECNET target host to monitor (default: MIM): MIM

=== PyDECNET Configuration ===
Locating PyDECNET binary...
Found PyDECNET at: /usr/local/bin/pydecnet
Use this path? (Y/n): y

=== Name Update Configuration ===
Enter update interval in hours (default: 48, 0 to disable): 48

=== Testing Email Configuration ===
Send a test email to verify configuration? (y/N): y
Sending test email...
✓ Email configuration test successful!

Configuration saved successfully!
```

### Automatic Name Updates

The daemon can automatically update DECNET node names from HECnet at configurable intervals:

- **Default**: Updates every 48 hours (2880 minutes)
- **Configure**: During setup, specify update interval in hours
- **Disable**: Set interval to 0 to disable automatic updates
- **Manual**: Use `python decnet-daemon.py --update-names` anytime

The daemon tracks the last update time and automatically downloads the latest node list when the configured interval has elapsed.

### 5. PyDECNET Configuration Details

The HECNET daemon will automatically discover your PyDECNET installation during the setup process. The setup script searches for PyDECNET using:

#### System Commands (Primary Method)
- **Linux/macOS**: `which pydecnet`
- **Windows**: `where pydecnet` and PowerShell `Get-Command pydecnet`

#### Common Installation Locations (Fallback)
- `~/hecnet/bin/pydecnet`
- `~/bin/pydecnet`
- `/usr/local/bin/pydecnet`
- `/usr/bin/pydecnet`
- `~/pydecnet/pydecnet`
- `~/DECnet/bin/pydecnet`
- `~/decnet/bin/pydecnet`

If PyDECNET is not found automatically, you'll be prompted to enter the path manually during setup.

### 6. Test the Setup

```bash
# Activate virtual environment if not already active
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Test manual restart
python decnet-daemon.py --relaunch

# Test DECNET name update
python decnet-daemon.py --update-names

# Check system status
python decnet-status.py
```

## Running the Daemon on Boot

For reliable PyDECNET monitoring, especially when away from your system, you'll want the daemon to start automatically on boot. Here are methods for different operating systems:

### Linux (systemd) - Recommended

Most modern Linux distributions use systemd. This is the preferred method for Linux systems.

#### Create the Service File

```bash
# Create service file
sudo nano /etc/systemd/system/hecnet-daemon.service
```

#### Service Configuration

Add the following content (replace `USERNAME` with your actual username):

```ini
[Unit]
Description=HECNET Daemon - PyDECNET Router Monitor
Documentation=https://github.com/mkostersitz/hecnet-daemon
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=forking
User=USERNAME
Group=USERNAME
WorkingDirectory=/home/USERNAME/hecnet-daemon
Environment=PATH=/home/USERNAME/hecnet-daemon/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/USERNAME/hecnet-daemon/venv/bin/python /home/USERNAME/hecnet-daemon/decnet-daemon.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal
SyslogIdentifier=hecnet-daemon

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=false
ReadWritePaths=/home/USERNAME/hecnet-daemon

[Install]
WantedBy=multi-user.target
```

#### Enable and Start

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable automatic startup
sudo systemctl enable hecnet-daemon

# Start the service now
sudo systemctl start hecnet-daemon

# Check status
sudo systemctl status hecnet-daemon
```

#### Service Management

```bash
# Check service status
sudo systemctl status hecnet-daemon

# View logs
sudo journalctl -u hecnet-daemon -f

# Stop service
sudo systemctl stop hecnet-daemon

# Disable auto-start
sudo systemctl disable hecnet-daemon

# Restart service
sudo systemctl restart hecnet-daemon
```

### Linux (crontab) - Alternative Method

If systemd is not available, use crontab:

```bash
# Edit user crontab
crontab -e

# Add this line to start daemon on boot
@reboot cd /home/USERNAME/hecnet-daemon && /home/USERNAME/hecnet-daemon/venv/bin/python decnet-daemon.py

# Or with logging
@reboot cd /home/USERNAME/hecnet-daemon && /home/USERNAME/hecnet-daemon/venv/bin/python decnet-daemon.py >> /home/USERNAME/hecnet-daemon/hecnet/logs/boot.log 2>&1
```

### macOS (LaunchAgent)

For macOS systems, use launchd:

#### Create Launch Agent

```bash
# Create the plist file
nano ~/Library/LaunchAgents/com.hecnet.daemon.plist
```

#### LaunchAgent Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hecnet.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/USERNAME/hecnet-daemon/venv/bin/python</string>
        <string>/Users/USERNAME/hecnet-daemon/decnet-daemon.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/USERNAME/hecnet-daemon</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/USERNAME/hecnet-daemon/hecnet/logs/daemon.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/USERNAME/hecnet-daemon/hecnet/logs/daemon-error.log</string>
</dict>
</plist>
```

#### Enable LaunchAgent

```bash
# Load the launch agent
launchctl load ~/Library/LaunchAgents/com.hecnet.daemon.plist

# Enable auto-start
launchctl enable gui/$(id -u)/com.hecnet.daemon

# Start now
launchctl start com.hecnet.daemon

# Check status
launchctl list | grep hecnet
```

### Windows (Task Scheduler)

For Windows systems, use Task Scheduler:

#### Create Scheduled Task

1. Open Task Scheduler (`taskschd.msc`)
2. Click "Create Basic Task..."
3. Name: "HECNET Daemon"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
6. Program: `C:\Python\python.exe` (your Python path)
7. Arguments: `C:\path\to\hecnet-daemon\decnet-daemon.py`
8. Start in: `C:\path\to\hecnet-daemon`

#### PowerShell Alternative

```powershell
# Create scheduled task via PowerShell
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\path\to\hecnet-daemon\decnet-daemon.py" -WorkingDirectory "C:\path\to\hecnet-daemon"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "HECNET Daemon" -Action $action -Trigger $trigger -Settings $settings -User $env:USERNAME
```

### Docker (Cross-Platform)

For containerized deployment:

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "decnet-daemon.py"]
```

#### Docker Compose

```yaml
version: '3.8'
services:
  hecnet-daemon:
    build: .
    container_name: hecnet-daemon
    restart: unless-stopped
    volumes:
      - ./pyvenv.cfg:/app/pyvenv.cfg:ro
      - ./hecnet/logs:/app/hecnet/logs
      - ./config:/app/config:ro
    environment:
      - TZ=UTC
```

### Verification

After setting up boot startup, verify it works:

```bash
# Reboot your system
sudo reboot

# After reboot, check if daemon is running
python decnet-status.py

# Or check process list
ps aux | grep decnet-daemon  # Linux/macOS
tasklist | findstr python    # Windows

# Check logs
tail -f hecnet/logs/decnet-status.log
```

### Troubleshooting Boot Issues

**Common Problems:**
- **Path Issues**: Ensure full paths are used in service files
- **Permissions**: Service must run as the user who configured the daemon
- **Network Timing**: Add delays if network isn't ready at boot
- **Virtual Environment**: Ensure correct Python interpreter path

**Debug Tips:**
```bash
# Test the exact command that will run at boot
cd /path/to/hecnet-daemon
/path/to/venv/bin/python decnet-daemon.py

# Check service logs (Linux)
sudo journalctl -u hecnet-daemon --since "5 minutes ago"

# Verify configuration
python setup.py  # Re-run setup if needed
```

**Why Run on Boot?**
Running the daemon on boot ensures continuous monitoring of your PyDECNET router, even after:
- System reboots
- Power outages  
- Network interruptions
- Automatic updates

This is essential for remote monitoring when you're away from your system and need reliable DECNET connectivity alerts.

## Updating Configuration

To update the configuration, run the setup script again:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Run setup to reconfigure
python setup.py

# Restart daemon to apply changes
python decnet-daemon.py --relaunch
```

## Next Steps

After installation, see the main [README.md](README.md) for:
- Usage instructions
- Manual operations
- Log file locations
- Troubleshooting guide
- Advanced configuration options
