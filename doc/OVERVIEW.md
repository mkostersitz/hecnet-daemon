# HECNET Daemon - Overview & Architecture

## Purpose & Mission

The HECNET Daemon is a comprehensive monitoring and management system designed to **keep your PyDECNET router running reliably even when you're away**. This autonomous system ensures continuous operation of your DECNET node by providing automated process management, connectivity monitoring, and proactive email notifications.
It runs pydecnet in daemon mode and keeps a close eye on it and the connection it serves. 

### The Remote Monitoring Problem

When running a PyDECNET router as part of the HECnet (Historic Ethernet Computer Network), several critical issues can occur:

- **Process Crashes**: PyDECNET may terminate unexpectedly due to network issues, configuration problems, power failure, or system resource constraints
- **Network Connectivity Loss**: DECNET links can fail due to internet connectivity issues, IP Address issues, remote node problems, or routing changes  
- **Silent Failures**: Problems can occur hours or days without notice, leaving your node unreachable
- **Maintenance Tasks**: Node names and routing tables need periodic updates from the central HECnet registry

### The Solution: Autonomous Monitoring

The HECNET Daemon solves these problems by providing:

1. **24/7 Process Monitoring**: Continuously watches PyDECNET and automatically restarts it when needed
2. **Link Status Monitoring**: Tests DECNET connectivity and detects network issues immediately
3. **Instant Email Alerts**: Sends notifications the moment problems occur or resolve
4. **Automatic Maintenance**: Keeps node names current with configurable update intervals
5. **Remote Accessibility**: Provides status information and logs for remote troubleshooting

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    HECNET Daemon System                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  Process        │  │  Link Status    │                  │
│  │  Monitor        │  │  Monitor        │                  │
│  │                 │  │                 │                  │
│  │ • Check PyDECNET│  │ • Test ncp      │                  │
│  │ • Auto restart  │  │ • Check target  │                  │
│  │ • Socket cleanup│  │ • Send alerts   │                  │
│  └─────────────────┘  └─────────────────┘                  │
│           │                     │                          │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │  Name Update    │  │  Email          │                  │
│  │  System         │  │  Notification   │                  │
│  │                 │  │                 │                  │
│  │ • Auto download │  │ • Gmail SMTP    │                  │
│  │ • Configurable  │  │ • Link status   │                  │
│  │ • Smart timing  │  │ • Process alerts│                  │
│  └─────────────────┘  └─────────────────┘                  │
├─────────────────────────────────────────────────────────────┤
│                    Configuration System                    │
├─────────────────────────────────────────────────────────────┤
│ • Interactive Setup  • Path Auto-Discovery                 │
│ • Email Configuration • PyDECNET Integration               │
│ • Update Scheduling  • Cross-Platform Support              │
└─────────────────────────────────────────────────────────────┘
```

### Monitoring Cycle

The daemon operates on a continuous monitoring cycle (default: 120 seconds):

1. **Process Check**: Verify PyDECNET is running
   - If not running → Automatic restart sequence
   - If running → Continue to next check

2. **Connectivity Test**: Test DECNET link to target host
   - Run `ncp sho node [target]` command
   - Check for "Unreachable" status
   - Send email alerts on status changes

3. **Name Update Check**: Evaluate if node names need updating
   - Compare current time with last update + configured interval
   - Download latest node list from HECnet if due
   - Update local PyDECNET configuration

4. **Status Logging**: Record all activities with timestamps
   - Process status and actions taken
   - Connectivity test results
   - Update schedules and completions

## Key Features & Benefits

### 1. Autonomous Process Management
- **Automatic Restart**: Detects when PyDECNET crashes and immediately restarts it
- **Socket Cleanup**: Removes locked sockets that prevent restart
- **Configuration Integrity**: Ensures PyDECNET starts with correct configuration files
- **Resource Management**: Monitors system resources and logs process information

### 2. Proactive Link Monitoring
- **Continuous Testing**: Regular connectivity tests to configured DECNET hosts
- **Immediate Detection**: Identifies link failures within minutes of occurrence  
- **Status Tracking**: Maintains history of connectivity status changes
- **Multi-Target Support**: Can monitor connectivity to any DECNET node (default: MIM)

### 3. Smart Email Notifications
- **Instant Alerts**: Email notifications sent immediately when issues occur
- **Status Updates**: Notifications when problems resolve automatically
- **Detailed Information**: Includes diagnostic output from DECNET commands
- **Gmail Integration**: Uses secure app passwords for reliable delivery

### 4. Automated Maintenance
- **Node Name Updates**: Automatically downloads latest HECnet node list
- **Configurable Timing**: Update intervals from 1 hour to weeks (default: 48 hours)
- **Smart Scheduling**: Only updates when actually needed
- **Error Handling**: Graceful handling of download failures with retry logic

### 5. Remote Monitoring Capabilities
- **Status Scripts**: Check daemon status remotely via `decnet-status.py`
- **Comprehensive Logging**: Detailed logs for troubleshooting from anywhere
- **Configuration Transparency**: Clear visibility into all settings and schedules
- **Manual Override**: Force operations remotely when needed

## Use Cases & Scenarios

### Scenario 1: Home Router While Traveling
You're running a PyDECNET router at home and traveling for a week:
- **Problem**: Router crashes on day 3, node becomes unreachable
- **Solution**: Daemon detects crash within 2 minutes, restarts PyDECNET, sends email confirmation
- **Result**: Node back online before you even know there was a problem

### Scenario 2: Internet Connection Issues  
Your home internet has intermittent connectivity problems:
- **Problem**: DECNET links go up and down, hard to track remotely
- **Solution**: Daemon monitors link status continuously, emails you each status change
- **Result**: Complete visibility into connectivity patterns, can contact ISP with specific timing data

### Scenario 3: Node Name Updates
HECnet adds new nodes and updates routing information monthly:
- **Problem**: Your router has outdated node names, can't reach new systems
- **Solution**: Daemon automatically downloads updates every 48 hours, keeps routing current
- **Result**: Always have latest routing information without manual intervention

### Scenario 4: System Maintenance
Your server needs reboots for security updates:
- **Problem**: PyDECNET doesn't restart automatically after reboot
- **Solution**: Daemon configured as systemd service, starts automatically, restarts PyDECNET
- **Result**: Router comes back online automatically after any system restart

## Technical Implementation

### Configuration Management
- **Interactive Setup**: `python setup.py` guides through all configuration
- **Persistent Storage**: Settings stored in `pyvenv.cfg` for portability
- **Path Auto-Discovery**: Automatically finds PyDECNET installation
- **Validation**: Comprehensive checks ensure configuration correctness

### Monitoring Engine
- **Python Daemon**: Uses `python-daemon` library for proper daemon behavior
- **Process Detection**: `psutil` library for robust process monitoring
- **Network Testing**: Native DECNET `ncp` commands for connectivity testing
- **Email Integration**: Standard SMTP with Gmail app password authentication

### File Organization
```
hecnet-daemon/
├── decnet-daemon.py          # Main daemon process
├── setup.py                  # Interactive configuration
├── decnet-status.py          # Status reporting tool
├── decnet-name-update.py     # Node name update utility
├── requirements.txt          # Python dependencies
├── pyvenv.cfg               # Configuration storage (auto-generated)
├── config/                  # PyDECNET configuration files
├── hecnet/logs/            # All log files and timestamps
└── doc/                    # Documentation
```

### Integration Points
- **PyDECNET**: Manages binary execution, configuration files, log redirection
- **System Services**: Can run as systemd service for automatic startup
- **Email Services**: Gmail SMTP integration with app password security
- **HECnet Registry**: Downloads node lists from official MIM server

## Operational Benefits

### For System Administrators
- **Reduced Downtime**: Automatic recovery from common failure modes
- **Proactive Monitoring**: Know about problems before users do
- **Maintenance Automation**: Routine tasks handled automatically
- **Historical Data**: Complete logs for trend analysis and troubleshooting

### For DECNET Enthusiasts  
- **Reliable Connectivity**: Node stays reachable even during problems
- **Current Routing**: Always have latest node names and routing data
- **Remote Peace of Mind**: Monitor your node from anywhere via email
- **Easy Setup**: Automatic configuration handles technical details

### For Network Operators
- **Network Stability**: Fewer nodes going offline unexpectedly
- **Faster Recovery**: Automatic restart reduces outage duration  
- **Better Diagnostics**: Detailed logging helps identify network issues
- **Consistent Updates**: All nodes stay current with registry changes

## Future Enhancements

The modular architecture supports easy expansion:

- **Multiple Target Monitoring**: Monitor connectivity to several DECNET hosts
- **Web Dashboard**: Browser-based status and control interface
- **Metrics Collection**: Prometheus/Grafana integration for trending
- **Mobile Notifications**: SMS or push notification options
- **Cluster Management**: Monitor multiple PyDECNET installations
- **Advanced Scheduling**: More sophisticated update and maintenance windows

## Getting Started

1. **Install**: Clone repository and install dependencies
2. **Configure**: Run `python setup.py` for interactive setup
3. **Test**: Verify operation with manual commands
4. **Deploy**: Install as system service for automatic startup
5. **Monitor**: Receive email alerts and check logs remotely

The HECNET Daemon transforms PyDECNET from a manual process requiring constant attention into a reliable, autonomous service that you can trust to operate correctly whether you're at home or traveling anywhere in the world.

---

*This daemon represents the evolution of network monitoring from reactive troubleshooting to proactive, automated management - ensuring your piece of computing history stays connected to the global HECnet community.*
