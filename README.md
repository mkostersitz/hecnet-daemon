# HECNET Daemon

A Python daemon for monitoring and managing PyDECNET processes and DECNET link status. This daemon automatically restarts PyDECNET when it goes down, monitors DECNET link connectivity, and sends email notifications when the link status changes.

**Perfect for remote PyDECNET router monitoring when you're away from your system.**

## Features

- **🔄 Process Monitoring**: Automatically detects when PyDECNET is not running and restarts it
- **🌐 Link Status Monitoring**: Checks DECNET link connectivity every 2 minutes
- **📧 Email Notifications**: Sends alerts when the DECNET link goes down or comes back up
- **🔄 Automatic Name Updates**: Downloads updated DECNET node names from HECnet at configurable intervals (default: 48 hours)
- **⚙️ Daemon Mode**: Runs as a background service
- **📝 Comprehensive Logging**: Detailed logs for troubleshooting and monitoring
- **🛠️ Manual Operations**: Support for manual restart and HECNET name updates
- **🚀 Auto-Discovery**: Automatically finds PyDECNET installation and configures paths
- **🔒 Secure Configuration**: Template-based config system keeps sensitive data local

## Quick Start

### Prerequisites
- Python 3.6+ 
- [PyDECNET installed and configured](https://github.com/pkoning2/pydecnet/blob/main/pydecnet/doc/install.txt)
- Gmail account with app password for notifications

### Installation
```bash
# Clone the repository
git clone https://github.com/mkostersitz/hecnet-daemon.git
cd hecnet-daemon

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure the daemon (interactive setup)
python setup.py

# Test the setup
python decnet-status.py
```

### Basic Usage
```bash
# Start the daemon
python decnet-daemon.py

# Manual operations
python decnet-daemon.py --relaunch      # Restart PyDECNET
python decnet-daemon.py --update-names  # Update node names
python decnet-status.py                 # Check status
```

## Documentation

| Document | Description |
|----------|-------------|
| **[📋 INSTALL.md](INSTALL.md)** | **Complete installation guide with platform-specific instructions** |
| [🏗️ doc/OVERVIEW.md](doc/OVERVIEW.md) | Detailed architecture and system overview |
| [🔄 doc/AUTOMATIC_NAME_UPDATES.md](doc/AUTOMATIC_NAME_UPDATES.md) | Automatic node name update system |
| [🔍 doc/PYDECNET_DISCOVERY.md](doc/PYDECNET_DISCOVERY.md) | PyDECNET binary auto-discovery system |
| [⚙️ doc/CONFIGURATION_MANAGEMENT.md](doc/CONFIGURATION_MANAGEMENT.md) | Configuration system and security |

## What This Daemon Does

The HECNET Daemon runs continuously in the background and:

1. **Monitors PyDECNET Process**: Checks every 2 minutes if PyDECNET is running
2. **Automatic Restart**: If PyDECNET crashes, immediately restarts it with proper configuration
3. **Link Monitoring**: Tests DECNET connectivity to your target host (default: MIM)
4. **Email Alerts**: Sends you email notifications when links go down or come back up
5. **Name Updates**: Automatically downloads latest HECnet node names (configurable interval)
6. **Comprehensive Logging**: Records all activities for troubleshooting

**Perfect for:** Remote monitoring of your PyDECNET router when you're traveling, at work, or away from your system.

## Running on Boot

For reliable remote monitoring, set up the daemon to start automatically on boot:

**Linux (systemd):**
```bash
# See INSTALL.md for complete systemd service setup
sudo nano /etc/systemd/system/hecnet-daemon.service
sudo systemctl enable hecnet-daemon
sudo systemctl start hecnet-daemon
```

**Other platforms:** See [INSTALL.md](INSTALL.md) for macOS, Windows, and Docker instructions.

## Usage

### Running as a Daemon

```bash
# Activate virtual environment
source venv/bin/activate

# Start the daemon
python decnet-daemon.py
```

The daemon will:
- Check if PyDECNET is running every 2 minutes
- Restart PyDECNET if it's not running
- Monitor DECNET link status to your target host
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

## Installation & Configuration

Complete installation instructions are available in [INSTALL.md](INSTALL.md), including:
- Environment setup
- Dependencies installation  
- Configuration steps
- Running on boot (systemd, LaunchAgent, Task Scheduler)

## Log Files

The daemon creates several log files for monitoring:

- **Status Log**: `./hecnet/logs/decnet-status.log` - Main daemon activity
- **Info Log**: `./hecnet/logs/decnet-launch-info.log` - PyDECNET stdout  
- **Error Log**: `./hecnet/logs/decnet-status-error.log` - PyDECNET stderr

```bash
# Watch logs in real-time
tail -f hecnet/logs/decnet-status.log

# Check status
python decnet-status.py
```

## Configuration Updates

To modify daemon settings:

```bash
# Reconfigure settings
python setup.py

# Apply changes  
python decnet-daemon.py --relaunch
```

## Dependencies

- **Python 3.6+**
- **psutil** (>=5.8.0): Process and system monitoring
- **python-daemon** (>=2.3.0): Daemon functionality

Full dependency information is in `requirements.txt`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Development setup
- Coding standards  
- Pull request process
- Testing requirements

## Support

For issues and support:
1. Check the [troubleshooting section](INSTALL.md#troubleshooting) in INSTALL.md
2. Review log files in `./hecnet/logs/`
3. Open an issue on the project repository


