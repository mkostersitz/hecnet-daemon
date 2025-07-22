# HECNET Daemon

A Python daemon for monitoring and managing PyDECNET processes and DECNET link status. This daemon automatically restarts PyDECNET when it goes down, monitors DECNET link connectivity, and sends email notifications when the link status changes.

## Features

- **Process Monitoring**: Automatically detects when PyDECNET is not running and restarts it
- **Link Status Monitoring**: Checks DECNET link to A2RTR node every 60 seconds
- **Email Notifications**: Sends alerts when the DECNET link goes down or comes back up
- **Daemon Mode**: Runs as a background service
- **Logging**: Comprehensive logging to files and stdout
- **Manual Operations**: Support for manual restart and HECNET name updates

## Prerequisites

- Linux operating system
- Python 3.6 or higher
- PyDECNET installed and configured
- sudo privileges (for process management and socket cleanup)
- Gmail account with app password for email notifications

## Setup Instructions

### 1. Clone or Download the Project

```bash
cd /home/mikek/  # or your preferred directory
git clone <repository-url> hecnet-daemon
cd hecnet-daemon
```

### 2. Create a Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Verify you're in the virtual environment
which python  # Should show path to venv/bin/python
```

### 3. Install Required Packages

```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt

# Verify installation
pip list
```

### 4. Configuration

#### Update Configuration Paths

Edit `hecnet-damon.py` and update the following paths to match your system:

```python
# Global paths and variables
PYDECNET_CONFIG_FILES = [
    "/home/yourusername/decnet/dev-logging.json",    # Update path
    "/home/yourusername/decnet/theark.conf",         # Update path
    "/home/yourusername/decnet/http.conf"            # Update path
]
LOG_INFO_PATH = "/home/yourusername/decnet/decnet-launch-info.log"
LOG_ERROR_PATH = "/home/yourusername/decnet/decnet-status-error.log"
STATUS_LOG_PATH = "/home/yourusername/decnet/decnet-status.log"
PYDECNET_BIN = "/home/yourusername/hecnet/bin/pydecnet"
HECNET_UPDATE_SCRIPT = "/home/yourusername/decnet/hecnetupdate.sh"
```

#### Configure Email Settings

Update the email configuration in `hecnet-damon.py`:

```python
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"  # Gmail app password, not regular password
RECEIVER_EMAIL = "recipient@example.com"
```

**Note**: For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an app password (not your regular password)
3. Use the app password in the script

### 5. Create Required Directories

```bash
# Create log directory if it doesn't exist
mkdir -p /home/yourusername/decnet

# Ensure the HECNET update script is executable
chmod +x /home/yourusername/decnet/hecnetupdate.sh
```

### 6. Test the Setup

```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Test manual restart
python hecnet-damon.py --relaunch

# Test HECNET update
python hecnet-damon.py --update-names
```

## Usage

### Running as a Daemon

```bash
# Activate virtual environment
source venv/bin/activate

# Start the daemon
python hecnet-damon.py
```

The daemon will:
- Check if PyDECNET is running every 60 seconds
- Restart PyDECNET if it's not running
- Monitor DECNET link status to A2RTR
- Send email notifications on link status changes
- Log all activities to the status log file

### Manual Operations

```bash
# Restart PyDECNET manually
python hecnet-damon.py --relaunch

# Update HECNET names
python hecnet-damon.py --update-names
```

### Running at System Startup

To run the daemon automatically at system startup, create a systemd service:

```bash
# Create service file
sudo nano /etc/systemd/system/hecnet-daemon.service
```

Add the following content:

```ini
[Unit]
Description=HECNET Daemon
After=network.target

[Service]
Type=forking
User=yourusername
Group=yourusername
WorkingDirectory=/home/yourusername/hecnet-daemon
Environment=PATH=/home/yourusername/hecnet-daemon/venv/bin
ExecStart=/home/yourusername/hecnet-daemon/venv/bin/python /home/yourusername/hecnet-daemon/hecnet-damon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable hecnet-daemon
sudo systemctl start hecnet-daemon

# Check status
sudo systemctl status hecnet-daemon
```

## Log Files

The daemon creates several log files:

- **Status Log**: `/home/yourusername/decnet/decnet-status.log` - Main daemon activity log
- **Info Log**: `/home/yourusername/decnet/decnet-launch-info.log` - PyDECNET stdout
- **Error Log**: `/home/yourusername/decnet/decnet-status-error.log` - PyDECNET stderr

Monitor logs in real-time:

```bash
# Watch main status log
tail -f /home/yourusername/decnet/decnet-status.log

# Watch all logs
tail -f /home/yourusername/decnet/*.log
```

## Troubleshooting

### Virtual Environment Issues

```bash
# If virtual environment is corrupted, recreate it
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Issues

```bash
# Ensure proper permissions for socket cleanup
sudo chown yourusername:yourusername /tmp/decnetapi.sock
```

### Email Not Working

1. Verify Gmail app password is correct
2. Check that 2-factor authentication is enabled
3. Test email settings with a simple script

### PyDECNET Not Starting

1. Check PyDECNET binary path
2. Verify configuration file paths
3. Check log files for error details
4. Ensure PyDECNET dependencies are installed

## Dependencies

- **psutil** (>=5.8.0): Process and system monitoring
- **python-daemon** (>=2.3.0): Daemon functionality

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions, check the log files first, then [add contact information or issue tracker].
