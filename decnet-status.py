#!/usr/bin/env python3
"""
DECNET Status Script

This script checks the status of the HECNET daemon and reports DECNET connectivity
to the command line. It provides a quick way to see if the daemon is running
and if DECNET is connected to the target host.
"""

import os
import sys
import time
import psutil
import subprocess
from datetime import datetime

def get_script_directory():
    """Get the directory where this script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def read_config_from_pyvenv():
    """Read configuration from pyvenv.cfg file."""
    script_dir = get_script_directory()
    pyvenv_path = os.path.join(script_dir, "pyvenv.cfg")
    
    config = {}
    if os.path.exists(pyvenv_path):
        with open(pyvenv_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    return config

def check_daemon_status():
    """Check if the HECNET daemon is running."""
    daemon_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Look for Python processes running decnet-daemon.py
            if (proc.info['name'] in ['python', 'python3'] and 
                proc.info['cmdline'] and 
                any('decnet-daemon.py' in arg for arg in proc.info['cmdline'])):
                daemon_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return daemon_processes

def check_pydecnet_status():
    """Check if PyDECNET process is running."""
    pydecnet_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'pydecnet' or (
                proc.info['cmdline'] and 
                any('pydecnet' in str(arg) for arg in proc.info['cmdline'])):
                pydecnet_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return pydecnet_processes

def check_decnet_connectivity(target_host):
    """Check DECNET connectivity to target host."""
    try:
        # Run the ncp command to check node status
        result = subprocess.run(
            ['ncp', 'sho', 'node', target_host.lower()],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            output = result.stdout
            if "Unreachable" in output:
                return False, "Unreachable", output
            else:
                return True, "Connected", output
        else:
            return False, "Command failed", result.stderr
            
    except subprocess.TimeoutExpired:
        return False, "Timeout", "Command timed out after 30 seconds"
    except FileNotFoundError:
        return False, "NCP not found", "ncp command not found - is PyDECNET installed?"
    except Exception as e:
        return False, "Error", str(e)

def get_log_tail(log_path, lines=5):
    """Get the last few lines from a log file."""
    if not os.path.exists(log_path):
        return "Log file not found"
    
    try:
        with open(log_path, 'r') as f:
            all_lines = f.readlines()
            return ''.join(all_lines[-lines:]).strip()
    except Exception as e:
        return f"Error reading log: {e}"

def format_uptime(process):
    """Format process uptime in a human-readable way."""
    try:
        create_time = process.create_time()
        uptime_seconds = time.time() - create_time
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    except:
        return "Unknown"

def print_status_header():
    """Print the status header."""
    print("=" * 60)
    print("HECNET Daemon Status Report")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def print_daemon_status(daemon_processes):
    """Print daemon status information."""
    print("🔧 HECNET Daemon Status:")
    print("-" * 30)
    
    if daemon_processes:
        print("✅ Daemon is RUNNING")
        for i, proc in enumerate(daemon_processes, 1):
            try:
                print(f"   Process {i}: PID {proc.pid}")
                print(f"   Uptime: {format_uptime(proc)}")
                print(f"   Memory: {proc.memory_info().rss / 1024 / 1024:.1f} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"   Process {i}: PID {proc.pid} (details unavailable)")
    else:
        print("❌ Daemon is NOT RUNNING")
        print("   To start: python decnet-daemon.py")
    
    print()

def print_pydecnet_status(pydecnet_processes):
    """Print PyDECNET status information."""
    print("🌐 PyDECNET Status:")
    print("-" * 20)
    
    if pydecnet_processes:
        print("✅ PyDECNET is RUNNING")
        for i, proc in enumerate(pydecnet_processes, 1):
            try:
                print(f"   Process {i}: PID {proc.pid}")
                print(f"   Uptime: {format_uptime(proc)}")
                print(f"   Memory: {proc.memory_info().rss / 1024 / 1024:.1f} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"   Process {i}: PID {proc.pid} (details unavailable)")
    else:
        print("❌ PyDECNET is NOT RUNNING")
        print("   The daemon should restart it automatically")
    
    print()

def print_connectivity_status(is_connected, status, output, target_host):
    """Print DECNET connectivity status."""
    print(f"🔗 DECNET Connectivity to {target_host}:")
    print("-" * 35)
    
    if is_connected:
        print("✅ CONNECTED")
    else:
        print("❌ DISCONNECTED")
    
    print(f"   Status: {status}")
    
    # Show relevant parts of the output
    if output and len(output) > 100:
        print("   Output (truncated):")
        lines = output.split('\n')
        for line in lines[:3]:  # Show first 3 lines
            if line.strip():
                print(f"     {line.strip()}")
        if len(lines) > 3:
            print("     ...")
    elif output:
        print(f"   Output: {output}")
    
    print()

def print_log_summary():
    """Print recent log entries."""
    script_dir = get_script_directory()
    log_dir = os.path.join(script_dir, "hecnet", "logs")
    status_log = os.path.join(log_dir, "decnet-status.log")
    
    print("📋 Recent Log Entries:")
    print("-" * 22)
    
    recent_logs = get_log_tail(status_log, 5)
    if recent_logs and recent_logs != "Log file not found":
        for line in recent_logs.split('\n'):
            if line.strip():
                print(f"   {line}")
    else:
        print("   No recent log entries found")
    
    print()

def print_configuration_info(config):
    """Print configuration information."""
    print("⚙️  Configuration:")
    print("-" * 16)
    
    target_host = config.get('hecnet_target_host', 'Not configured')
    sender_email = config.get('hecnet_sender_email', 'Not configured')
    receiver_email = config.get('hecnet_receiver_email', 'Not configured')
    
    print(f"   Target Host: {target_host}")
    print(f"   Sender Email: {sender_email}")
    print(f"   Receiver Email: {receiver_email}")
    
    if target_host == 'Not configured':
        print("   ⚠️  Run 'python setup.py' to configure")
    
    print()

def main():
    """Main status checking function."""
    print_status_header()
    
    # Read configuration
    config = read_config_from_pyvenv()
    target_host = config.get('hecnet_target_host', 'MIM')
    
    # Check daemon status
    daemon_processes = check_daemon_status()
    print_daemon_status(daemon_processes)
    
    # Check PyDECNET status
    pydecnet_processes = check_pydecnet_status()
    print_pydecnet_status(pydecnet_processes)
    
    # Check DECNET connectivity
    is_connected, status, output = check_decnet_connectivity(target_host)
    print_connectivity_status(is_connected, status, output, target_host)
    
    # Show configuration
    print_configuration_info(config)
    
    # Show recent logs
    print_log_summary()
    
    # Summary
    print("📊 Summary:")
    print("-" * 10)
    daemon_status = "✅ Running" if daemon_processes else "❌ Stopped"
    pydecnet_status = "✅ Running" if pydecnet_processes else "❌ Stopped"
    connectivity_status = "✅ Connected" if is_connected else "❌ Disconnected"
    
    print(f"   Daemon: {daemon_status}")
    print(f"   PyDECNET: {pydecnet_status}")
    print(f"   Connectivity: {connectivity_status}")
    
    # Exit code based on overall status
    if daemon_processes and pydecnet_processes and is_connected:
        print("\n🎉 All systems operational!")
        sys.exit(0)
    elif not daemon_processes:
        print("\n⚠️  Daemon not running - start with: python decnet-daemon.py")
        sys.exit(1)
    elif not is_connected:
        print(f"\n⚠️  DECNET connectivity to {target_host} is down")
        sys.exit(2)
    else:
        print("\n⚠️  Some issues detected")
        sys.exit(3)

if __name__ == "__main__":
    main()
