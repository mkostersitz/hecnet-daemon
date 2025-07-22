#!/usr/bin/env python3
"""
HECNET Daemon Setup Script

This script configures the HECNET daemon by prompting for email settings
and DECNET configuration, then saves them to pyvenv.cfg for use by the daemon.
"""

import os
import sys
import configparser
import getpass
import subprocess
import importlib.util
from pathlib import Path

def get_script_directory():
    """Get the directory where this script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def check_requirements():
    """Check if required packages from requirements.txt are installed."""
    script_dir = get_script_directory()
    requirements_path = os.path.join(script_dir, "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print("WARNING: requirements.txt not found!")
        return False
    
    print("\n=== Checking Python Dependencies ===")
    
    # Read requirements.txt
    missing_packages = []
    try:
        with open(requirements_path, 'r') as f:
            requirements = f.readlines()
        
        for req in requirements:
            req = req.strip()
            if req and not req.startswith('#'):
                # Extract package name (ignore version constraints)
                package_name = req.split('>=')[0].split('==')[0].split('<')[0].split('>')[0]
                
                # Check if package is importable
                try:
                    if package_name == 'python-daemon':
                        # Special case for python-daemon which imports as 'daemon'
                        import daemon
                        print(f"✓ {package_name} is installed")
                    elif package_name == 'psutil':
                        import psutil
                        print(f"✓ {package_name} is installed")
                    else:
                        # Generic import check
                        spec = importlib.util.find_spec(package_name)
                        if spec is not None:
                            print(f"✓ {package_name} is installed")
                        else:
                            missing_packages.append(package_name)
                            print(f"✗ {package_name} is NOT installed")
                except ImportError:
                    missing_packages.append(package_name)
                    print(f"✗ {package_name} is NOT installed")
    
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")
        return False
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
        
        install_now = input("\nInstall missing packages now? (y/N): ").strip().lower()
        if install_now == 'y':
            try:
                print("Installing packages...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path], 
                             check=True, capture_output=False)
                print("✓ Packages installed successfully!")
                return True
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install packages: {e}")
                return False
        else:
            print("Please install the required packages before running the daemon.")
            return False
    else:
        print("✓ All required packages are installed!")
        return True

def read_pyvenv_cfg(pyvenv_path):
    """Read the existing pyvenv.cfg file and return its contents."""
    config = {}
    if os.path.exists(pyvenv_path):
        with open(pyvenv_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config

def write_pyvenv_cfg(pyvenv_path, config):
    """Write the configuration back to pyvenv.cfg file."""
    with open(pyvenv_path, 'w') as f:
        f.write("# Python Virtual Environment Configuration\n")
        f.write("# Standard pyvenv settings\n")
        for key, value in config.items():
            if key in ['home', 'include-system-site-packages', 'version', 'executable', 'command']:
                f.write(f"{key} = {value}\n")
        
        f.write("\n# HECNET Daemon Configuration\n")
        f.write("# Email notification settings\n")
        for key, value in config.items():
            if key.startswith('hecnet_'):
                f.write(f"{key} = {value}\n")

def prompt_for_email_config():
    """Prompt user for email configuration."""
    print("\n=== Email Configuration ===")
    print("Configure email settings for notifications when DECNET link status changes.")
    print("Note: For Gmail, you'll need to use an app password, not your regular password.")
    print("See: https://support.google.com/accounts/answer/185833")
    
    sender_email = input("\nEnter sender email address (Gmail recommended): ").strip()
    while not sender_email or '@' not in sender_email:
        print("Please enter a valid email address.")
        sender_email = input("Enter sender email address: ").strip()
    
    print(f"\nFor Gmail account '{sender_email}', you need an app password.")
    print("1. Enable 2-factor authentication on your Gmail account")
    print("2. Generate an app password (not your regular password)")
    print("3. Use that app password below")
    
    sender_password = getpass.getpass("\nEnter email app password (input hidden): ").strip()
    while not sender_password:
        print("Password cannot be empty.")
        sender_password = getpass.getpass("Enter email app password: ").strip()
    
    receiver_email = input("\nEnter receiver email address (where alerts will be sent): ").strip()
    while not receiver_email or '@' not in receiver_email:
        print("Please enter a valid email address.")
        receiver_email = input("Enter receiver email address: ").strip()
    
    return sender_email, sender_password, receiver_email

def prompt_for_decnet_config():
    """Prompt user for DECNET configuration."""
    print("\n=== DECNET Configuration ===")
    print("Configure the DECNET node to monitor for connectivity.")
    
    default_host = "MIM"
    decnet_host = input(f"Enter DECNET host to monitor (default: {default_host}): ").strip()
    if not decnet_host:
        decnet_host = default_host
    
    print(f"\nThe daemon will monitor connectivity to: {decnet_host}")
    print("It will run 'ncp sho node {decnet_host}' and check for 'Unreachable' status.")
    
    return decnet_host

def test_email_config(sender_email, sender_password, receiver_email):
    """Test email configuration by sending a test email."""
    print("\n=== Testing Email Configuration ===")
    test_email = input("Send a test email to verify configuration? (y/N): ").strip().lower()
    
    if test_email == 'y':
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            print("Sending test email...")
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "HECNET Daemon Setup - Test Email"
            
            body = """This is a test email from the HECNET Daemon setup script.

If you receive this email, your email configuration is working correctly.

The HECNET daemon will send notifications to this address when:
- DECNET link goes down
- DECNET link comes back up

Setup completed successfully!"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            
            print("✓ Test email sent successfully!")
            print(f"Check {receiver_email} for the test message.")
            
        except Exception as e:
            print(f"✗ Failed to send test email: {e}")
            print("Please check your email settings and try again.")
            return False
    
    return True

def main():
    """Main setup function."""
    print("HECNET Daemon Setup Script")
    print("=" * 40)
    
    script_dir = get_script_directory()
    pyvenv_path = os.path.join(script_dir, "pyvenv.cfg")
    
    print(f"Working directory: {script_dir}")
    print(f"Configuration file: {pyvenv_path}")
    
    # Check if required packages are installed
    if not check_requirements():
        print("\n✗ Setup cannot continue without required packages.")
        sys.exit(1)
    
    # Read existing configuration
    config = read_pyvenv_cfg(pyvenv_path)
    
    # Check if already configured
    if 'hecnet_sender_email' in config:
        print(f"\nExisting configuration found:")
        print(f"  Sender Email: {config.get('hecnet_sender_email', 'Not set')}")
        print(f"  Receiver Email: {config.get('hecnet_receiver_email', 'Not set')}")
        print(f"  DECNET Host: {config.get('hecnet_target_host', 'Not set')}")
        
        reconfigure = input("\nReconfigure settings? (y/N): ").strip().lower()
        if reconfigure != 'y':
            print("Setup cancelled. Existing configuration unchanged.")
            return
    
    # Get email configuration
    sender_email, sender_password, receiver_email = prompt_for_email_config()
    
    # Get DECNET configuration
    decnet_host = prompt_for_decnet_config()
    
    # Update configuration
    config['hecnet_sender_email'] = sender_email
    config['hecnet_sender_password'] = sender_password
    config['hecnet_receiver_email'] = receiver_email
    config['hecnet_target_host'] = decnet_host
    
    # Test email configuration
    if not test_email_config(sender_email, sender_password, receiver_email):
        print("\nEmail test failed. Configuration will still be saved.")
        proceed = input("Continue with setup? (y/N): ").strip().lower()
        if proceed != 'y':
            print("Setup cancelled.")
            return
    
    # Write configuration
    try:
        write_pyvenv_cfg(pyvenv_path, config)
        print(f"\n✓ Configuration saved to {pyvenv_path}")
        
        print("\n=== Setup Complete ===")
        print("Configuration saved successfully!")
        print("\nNext steps:")
        print("1. Ensure your PyDECNET configuration files are in the 'config/' directory")
        print("2. Make sure the hecnetupdate.sh script is executable: chmod +x config/hecnetupdate.sh")
        print("3. Test the daemon with: python decnet-daemon.py --relaunch")
        print("4. Start monitoring: python decnet-daemon.py")
        
        print(f"\nThe daemon will monitor DECNET connectivity to: {decnet_host}")
        print(f"Email notifications will be sent to: {receiver_email}")
        
    except Exception as e:
        print(f"\n✗ Failed to save configuration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
