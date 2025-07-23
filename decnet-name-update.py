#!/usr/bin/env python3
"""
DECNET Name Update Script

This script downloads the HECnet node list from MIM and generates a node names
configuration file for PyDECNET. It uses the same configuration system as the
HECNET daemon for consistency.

Based on the original hecnetupd.sh script by Supratim Sanyal.
Converted to Python for better integration with the HECNET daemon project.
"""

import os
import sys
import urllib.request
import urllib.error
import re
import socket
from datetime import datetime
from pathlib import Path

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

def get_user_home_directory():
    """Get the user's home directory in a cross-platform way."""
    return str(Path.home())

def get_output_directory():
    """Get the output directory for the node names file."""
    home_dir = get_user_home_directory()
    
    # Try to create .local/bin if it doesn't exist (common on Linux)
    local_bin_dir = os.path.join(home_dir, ".local", "bin")
    
    try:
        os.makedirs(local_bin_dir, exist_ok=True)
        return local_bin_dir
    except (OSError, PermissionError):
        # Fallback to home directory if .local/bin can't be created
        print(f"Warning: Could not create {local_bin_dir}, using home directory")
        return home_dir

def download_node_list(url="http://mim.stupi.net/hecnod", timeout=30):
    """Download the HECnet node list from MIM."""
    print(f"Downloading HECnet node list from {url}...")
    
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            content = response.read().decode('utf-8', errors='ignore')
            print(f"Successfully downloaded {len(content)} bytes")
            return content
    except urllib.error.URLError as e:
        print(f"Error downloading node list: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error downloading node list: {e}")
        return None

def parse_node_list(content):
    """Parse the downloaded node list and extract valid node entries."""
    if not content:
        return []
    
    nodes = []
    
    # Split into lines and process each one
    for line in content.splitlines():
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Look for lines that start with a number (node entries)
        if re.match(r'^\d', line):
            # Extract node information using regex
            # Format is typically: "1.13 (MIM) Reachable" or similar
            match = re.match(r'^(\d+\.\d+)\s+\(([^)]+)\).*', line)
            if match:
                node_addr = match.group(1)
                node_name = match.group(2).strip()
                
                # Validate node address format
                if re.match(r'^\d+\.\d+$', node_addr) and node_name:
                    nodes.append((node_addr, node_name))
                    print(f"Found node: {node_addr} ({node_name})")
                else:
                    print(f"Skipped invalid entry: {line}")
            else:
                print(f"Skipped unparseable line: {line}")
    
    return nodes

def generate_nodenames_file(nodes, output_path):
    """Generate the nodenames.conf file for PyDECNET."""
    hostname = socket.gethostname()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Generating node names file: {output_path}")
    
    try:
        with open(output_path, 'w') as f:
            # Write header
            f.write(f"# HECnet Node List: {timestamp} generated on {hostname}\n")
            
            # Always include MIM as the first entry
            f.write("node 1.13  MIM\n")
            
            # Write all discovered nodes
            for node_addr, node_name in sorted(nodes, key=lambda x: tuple(map(int, x[0].split('.')))):
                # Skip MIM since we already added it
                if node_addr == "1.13":
                    continue
                
                # Format: node ADDRESS  NAME
                f.write(f"node {node_addr}  {node_name}\n")
        
        print(f"Successfully wrote {len(nodes)} nodes to {output_path}")
        return True
        
    except (OSError, IOError) as e:
        print(f"Error writing to {output_path}: {e}")
        return False

def validate_configuration():
    """Validate that the configuration is present (optional for this script)."""
    config = read_config_from_pyvenv()
    
    # This script doesn't require email configuration, but we can check if it's set up
    if 'hecnet_sender_email' in config:
        print(f"Using configuration for target host: {config.get('hecnet_target_host', 'MIM')}")
    else:
        print("Note: HECNET daemon not configured. This script works independently.")
    
    return config

def main():
    """Main function."""
    print("DECNET Name Update Script")
    print("=" * 40)
    print("Downloading HECnet node list and generating PyDECNET configuration...")
    print()
    
    # Validate configuration (optional)
    config = validate_configuration()
    
    # Get output directory
    output_dir = get_output_directory()
    output_file = os.path.join(output_dir, "nodenames.conf")
    
    print(f"Output directory: {output_dir}")
    print(f"Output file: {output_file}")
    print()
    
    # Download the node list
    content = download_node_list()
    if not content:
        print("Failed to download node list. Exiting.")
        sys.exit(1)
    
    # Parse the node list
    nodes = parse_node_list(content)
    if not nodes:
        print("No valid nodes found in the downloaded list. Exiting.")
        sys.exit(1)
    
    print(f"\nFound {len(nodes)} valid nodes")
    
    # Generate the output file
    if generate_nodenames_file(nodes, output_file):
        print(f"\n✓ Successfully generated {output_file}")
        print(f"✓ Added {len(nodes)} nodes to the configuration")
        
        # Show some statistics
        unique_areas = set(addr.split('.')[0] for addr, _ in nodes)
        print(f"✓ Nodes span {len(unique_areas)} different areas")
        
        print("\nThe nodenames.conf file is ready for use with PyDECNET.")
        print("Make sure to configure PyDECNET to use this file for node name resolution.")
    else:
        print("\n✗ Failed to generate the node names file")
        sys.exit(1)

if __name__ == "__main__":
    main()
