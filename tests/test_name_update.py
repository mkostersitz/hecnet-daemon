#!/usr/bin/env python3
"""
Test script for automatic name update functionality.
This script tests the timing and configuration logic without running the full daemon.
"""

import os
from datetime import datetime, timedelta

def read_config_from_pyvenv():
    """Read configuration from pyvenv.cfg file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
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

def test_name_update_logic():
    """Test the automatic name update logic."""
    print("=== Automatic Name Update Test ===")
    
    # Read configuration
    config = read_config_from_pyvenv()
    name_update_interval = int(config.get('hecnet_name_update_interval', 2880))  # Default to 48 hours
    
    print(f"Configured update interval: {name_update_interval} minutes ({name_update_interval/60} hours)")
    
    if name_update_interval <= 0:
        print("✓ Automatic name updates are DISABLED")
        return
    
    # Check timestamp file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "hecnet", "logs")
    timestamp_file = os.path.join(log_dir, "last_name_update.txt")
    
    print(f"Timestamp file location: {timestamp_file}")
    
    if os.path.exists(timestamp_file):
        try:
            with open(timestamp_file, 'r') as f:
                timestamp_str = f.read().strip()
                last_update = datetime.fromisoformat(timestamp_str)
            print(f"Last update time: {last_update}")
        except Exception as e:
            print(f"Error reading timestamp: {e}")
            last_update = datetime.fromtimestamp(0)
            print("Using epoch time as fallback")
    else:
        print("No timestamp file found - first run")
        last_update = datetime.fromtimestamp(0)
    
    # Calculate timing
    current_time = datetime.now()
    time_since_update = current_time - last_update
    interval_seconds = name_update_interval * 60
    
    print(f"Current time: {current_time}")
    print(f"Time since last update: {time_since_update}")
    print(f"Hours since last update: {time_since_update.total_seconds() / 3600:.1f}")
    
    if time_since_update.total_seconds() >= interval_seconds:
        print("✅ UPDATE NEEDED - Time for automatic name update!")
    else:
        next_update_time = last_update + timedelta(minutes=name_update_interval)
        time_until_next = next_update_time - current_time
        hours_until_next = time_until_next.total_seconds() / 3600
        
        print(f"❌ Update not needed yet")
        print(f"Next update scheduled: {next_update_time}")
        print(f"Time until next update: {hours_until_next:.1f} hours")

if __name__ == "__main__":
    test_name_update_logic()
