# HECNET Daemon

A Python daemon for monitoring and managing PyDECNET processes and DECNET link status. This daemon automatically restarts PyDECNET when it goes down, monitors DECNET link connectivity, and sends email notifications when the link status changes.

## Features

- **Process Monitoring**: Automatically detects when PyDECNET is not running and restarts it
- **Link Status Monitoring**: Checks DECNET link to A2RTR node every 60 seconds
- **Email Notifications**: Sends alerts when the DECNET link goes down or comes back up
- **Automatic Name Updates**: Downloads updated DECNET node names from HECnet at configurable intervals (default: 48 hours)
- **Daemon Mode**: Runs as a background service
- **Logging**: Comprehensive logging to files and stdout
- **Manual Operations**: Support for manual restart and HECNET name updates

## Prerequisites

- Linux operating system
- Python 3.6 or higher
- **PyDECNET installed and configured** - See [PyDECNET Installation Guide](https://github.com/pkoning2/pydecnet/blob/main/pydecnet/doc/install.txt)
- sudo privileges (for process management and socket cleanup)
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

## Setup Instructions

### 1. Clone or Download the Project

```bash
cd ~  # or your preferred directory
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
SENDER_PASSWORD = "your-app-password"  # Gmail app password, not regular password
```

This will interactively configure:
- Email settings (sender, receiver, Gmail app password)
- Target DECNET host to monitor (default: MIM)
- **Automatic name updates** (default: every 48 hours, configurable)
- Automatically test email configuration

### Automatic Name Updates

The daemon can automatically update DECNET node names from HECnet at configurable intervals:

- **Default**: Updates every 48 hours (2880 minutes)
- **Configure**: During setup, specify update interval in hours
- **Disable**: Set interval to 0 to disable automatic updates
- **Manual**: Use `python decnet-daemon.py --update-names` anytime

The daemon tracks the last update time and automatically downloads the latest node list when the configured interval has elapsed.

### 5. PyDECNET Configuration

The HECNET daemon will automatically discover your PyDECNET installation during the setup process. The setup script searches for PyDECNET in:

- System PATH (using `which pydecnet` or `where pydecnet`)
- Common installation locations:
  - `~/hecnet/bin/pydecnet`
  - `~/bin/pydecnet`
  - `/usr/local/bin/pydecnet`
  - `/usr/bin/pydecnet`

If PyDECNET is not found automatically, you'll be prompted to enter the path manually during setup.

```bash
# Verify PyDECNET is accessible
which pydecnet
# or test the discovery system
python test_find_pydecnet.py
```

### 6. Test the Setup

```bash
# Activate virtual environment if not already active
source hecnet/bin/activate

# Test manual restart
python decnet-daemon.py --relaunch

# Test DECNET name update
python decnet-daemon.py --update-names

# Check system status
python decnet-status.py
```

## Usage

### Running as a Daemon

```bash
# Activate virtual environment
source venv/bin/activate

# Start the daemon
python decnet-daemon.py
```

The daemon will:
- Check if PyDECNET is running every 60 seconds
- Restart PyDECNET if it's not running
- Monitor DECNET link status to A2RTR
- **Automatically update DECNET node names** at the configured interval (default: 48 hours)
- Send email notifications on link status changes
- Log all activities to the status log file

### Manual Operations

```bash
# Restart PyDECNET manually
python decnet-daemon.py --relaunch

# Update DECNET names
python decnet-daemon.py --update-names

# Check system status
python decnet-status.py
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
User=$USER
Group=$USER
WorkingDirectory=%h/hecnet-daemon
Environment=PATH=%h/hecnet-daemon/hecnet/bin
ExecStart=%h/hecnet-daemon/hecnet/bin/python %h/hecnet-daemon/decnet-daemon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Note**: The `%h` variable automatically expands to the user's home directory, making the service portable across different users.

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable hecnet-daemon
sudo systemctl start hecnet-daemon

# Check status
sudo systemctl status hecnet-daemon
```

## Log Files

The daemon creates several log files in the project directory:

- **Status Log**: `./hecnet/logs/decnet-status.log` - Main daemon activity log
- **Info Log**: `./hecnet/logs/decnet-launch-info.log` - PyDECNET stdout
- **Error Log**: `./hecnet/logs/decnet-status-error.log` - PyDECNET stderr

Monitor logs in real-time:

```bash
# Watch main status log
tail -f hecnet/logs/decnet-status.log

# Watch all logs
tail -f hecnet/logs/*.log

# Check status with the status script
python decnet-status.py
```

## Updating the configuration

To update the configuration run `python3 ./setup.py` inside the virtual environment.   
Once the changes are configured run `python3 ./decnet-daemon.py --relaunch` to refresh the configuration.

## Troubleshooting

### Virtual Environment Issues

```bash
# If virtual environment is corrupted, recreate it
rm -rf hecnet
python3 -m venv hecnet
source hecnet/bin/activate
pip install -r requirements.txt
```

### Permission Issues

```bash
# Ensure proper permissions for socket cleanup
sudo chown $USER:$USER /tmp/decnetapi.sock
```

### Email Not Working

1. Run `python setup.py` to reconfigure email settings
2. Test with the built-in email test feature
3. Verify Gmail app password is correct
4. Check that 2-factor authentication is enabled

### PyDECNET Not Starting

1. Verify PyDECNET is installed at `~/hecnet/bin/pydecnet`
2. Check that configuration files are in the `config/` directory
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
