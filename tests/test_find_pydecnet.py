#!/usr/bin/env python3
"""
Test script to verify PyDECNET binary discovery functionality.
"""

import os
import subprocess
import platform

def find_pydecnet_binary():
    """Try to find the PyDECNET binary automatically using system commands."""
    print("Testing PyDECNET binary discovery...")
    
    system = platform.system().lower()
    print(f"Operating System: {platform.system()}")
    
    try:
        if system == "windows":
            # Try 'where' command first on Windows
            print("Trying 'where pydecnet' command...")
            try:
                result = subprocess.run(['where', 'pydecnet'], 
                                      capture_output=True, text=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("'where' command failed, trying PowerShell Get-Command...")
                result = subprocess.run(['powershell', '-Command', 'Get-Command pydecnet | Select-Object -ExpandProperty Source'], 
                                      capture_output=True, text=True, check=True)
        else:
            # Use 'which' command on Linux/macOS (more reliable than 'whereis')
            print("Trying 'which pydecnet' command...")
            result = subprocess.run(['which', 'pydecnet'], 
                                  capture_output=True, text=True, check=True)
        
        # Return the first path found (strip whitespace)
        path = result.stdout.strip().split('\n')[0]
        print(f"System command found: {path}")
        
        if path and os.path.exists(path) and os.access(path, os.X_OK):
            print(f"✅ Found executable PyDECNET at: {path}")
            return path
        else:
            print(f"❌ Path found but not executable: {path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ System command failed: {e}")
    except FileNotFoundError:
        print("❌ System command not found")
    
    # Fall back to checking common installation paths
    print("\nFalling back to manual path search...")
    possible_paths = [
        os.path.expanduser("~/hecnet/bin/pydecnet"),
        os.path.expanduser("~/bin/pydecnet"),
        "/usr/local/bin/pydecnet",
        "/usr/bin/pydecnet",
        os.path.expanduser("~/pydecnet/pydecnet"),
        os.path.expanduser("~/DECnet/bin/pydecnet"),
        os.path.expanduser("~/decnet/bin/pydecnet")
    ]
    
    for path in possible_paths:
        print(f"Checking: {path}")
        if os.path.exists(path) and os.access(path, os.X_OK):
            print(f"✅ Found executable PyDECNET at: {path}")
            return path
        elif os.path.exists(path):
            print(f"❌ File exists but not executable: {path}")
        else:
            print(f"❌ File not found: {path}")
    
    print("❌ PyDECNET binary not found")
    return None

if __name__ == "__main__":
    result = find_pydecnet_binary()
    if result:
        print(f"\n🎉 SUCCESS: PyDECNET found at: {result}")
    else:
        print(f"\n❌ FAILED: PyDECNET binary not found")
