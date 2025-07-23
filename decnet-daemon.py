import os
import sys  # Ensures sys is included for exit functionality
import time
import smtplib
from email.mime.text import MIMEText # Enable Email sending for server down
from email.mime.multipart import MIMEMultipart # Enable Email sending for server down
import psutil
from datetime import datetime, timedelta
import argparse
import daemon
import subprocess
from pathlib import Path

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

def validate_configuration():
    """Validate that required configuration is present."""
    required_keys = ['hecnet_sender_email', 'hecnet_sender_password', 'hecnet_receiver_email', 'hecnet_target_host', 'hecnet_pydecnet_bin']
    missing_keys = []
    
    for key in required_keys:
        if key not in CONFIG or not CONFIG[key] or CONFIG[key] in ['your-email@gmail.com', 'your-app-password', 'recipient@example.com']:
            missing_keys.append(key)
    
    if missing_keys:
        print("ERROR: HECNET daemon configuration is incomplete!")
        print("Missing or default values for:")
        for key in missing_keys:
            print(f"  - {key}")
        print("\nPlease run the setup script first:")
        print("  python setup.py")
        sys.exit(1)
    
    # Check if PyDECNET binary exists
    if not os.path.exists(PYDECNET_BIN):
        print(f"ERROR: PyDECNET binary not found at: {PYDECNET_BIN}")
        print("\nPlease run the setup script to reconfigure:")
        print("  python setup.py")
        sys.exit(1)
    
    # Log configuration info
    if NAME_UPDATE_INTERVAL > 0:
        hours = NAME_UPDATE_INTERVAL / 60
        log_message(f"Automatic name updates enabled: every {hours} hours")
    else:
        log_message("Automatic name updates disabled")

# Read configuration from pyvenv.cfg
CONFIG = read_config_from_pyvenv()

# Global paths and variables
DAEMON_VERSION = CONFIG.get('hecnet_daemon_version', '1.0')
SENDER_EMAIL = CONFIG.get('hecnet_sender_email', 'your-email@gmail.com')
SENDER_PASSWORD = CONFIG.get('hecnet_sender_password', 'your-app-password')
RECEIVER_EMAIL = CONFIG.get('hecnet_receiver_email', 'recipient@example.com')
TARGET_HOST = CONFIG.get('hecnet_target_host', 'MIM')
SLEEP_TIME = CONFIG.get('hecnet_sleep_time', 120)  # Default to 120 seconds if not set
NAME_UPDATE_INTERVAL = int(CONFIG.get('hecnet_name_update_interval', 2880))  # Default to 48 hours (2880 minutes)

# Get the directory of the current script and construct paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(SCRIPT_DIR, "hecnet")
LOG_DIR = os.path.join(VENV_DIR, "logs")
CONFIG_DIR = os.path.join(SCRIPT_DIR, "config")

# Create logs and config directories if they don't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

PYDECNET_CONFIG_FILES = [
    os.path.join(CONFIG_DIR, "dev-logging.json"),
    os.path.join(CONFIG_DIR, "theark.conf"),
    os.path.join(CONFIG_DIR, "http.conf")
]
LOG_INFO_PATH = os.path.join(LOG_DIR, "decnet-launch-info.log")
LOG_ERROR_PATH = os.path.join(LOG_DIR, "decnet-status-error.log")
STATUS_LOG_PATH = os.path.join(LOG_DIR, "decnet-status.log")
SOCKET_PATH = "/tmp/decnetapi.sock"
USER_HOME = str(Path.home())
PYDECNET_BIN = CONFIG.get('hecnet_pydecnet_bin', os.path.join(USER_HOME, "hecnet", "bin", "pydecnet"))
DECNET_NAME_UPDATE_SCRIPT = os.path.join(SCRIPT_DIR, "decnet-name-update.py")
NAME_UPDATE_TIMESTAMP_FILE = os.path.join(LOG_DIR, "last_name_update.txt")

# Function to log messages to both stdout and a file
def log_message(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} {message}"
    print(log_entry)
    try:
        with open(STATUS_LOG_PATH, "a") as log_file:
            log_file.write(log_entry + "\n")
    except Exception as e:
        print(f"[ERROR] Failed to write to log file: {e}")

# Function to send an email notification
def send_email(output, isDown):
    log_message("Sending email notification.")
    if isDown:
        subject = f"DECNET link to {TARGET_HOST} is down"
        body = f"The DECNET link to {TARGET_HOST} is down. Here is the output of 'ncp sho node {TARGET_HOST.lower()}':\n\n{output}"
    else:
        subject = f"DECNET link to {TARGET_HOST} is up"
        body = f"The DECNET link to {TARGET_HOST} is up. Here is the output of 'ncp sho node {TARGET_HOST.lower()}':\n\n{output}"

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        log_message("Email sent successfully.")
    except Exception as e:
        log_message(f"Failed to send email: {e}")

# Function to check the DECNET link
def check_decnet_link():
    log_message(f"Checking DECNET link status to {TARGET_HOST}.")
    result = os.popen(f"ncp sho node {TARGET_HOST.lower()}").read()
    if "Unreachable" in result:
        send_email(result, True)
        log_message(f"DECNET link to {TARGET_HOST} is down")
    else:
        log_message(f"DECNET link to {TARGET_HOST} is up.")

# Function to stop PyDECNET if running
def stop_pydecnet():
    log_message("Stopping PyDECNET process if it is running.")
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'pydecnet':
            log_message(f"PyDECNET is running. Stopping it (PID: {proc.info['pid']}).")
           # proc.terminate()
           # proc.wait()
            subprocess.run(["sudo", "pkill", "-f", "pydecnet"], check=True)

# Function to remove locked socket
def remove_locked_socket():
    log_message("Checking for locked socket.")
    if os.path.exists(SOCKET_PATH):
        log_message("PyDECNET Socket is locked. Removing it.")
        try:
            # os.remove(SOCKET_PATH)
            subprocess.run(["sudo", "rm", "/tmp/decnetapi.sock"], check=True)
        except Exception as e:
            log_message(f"Failed to remove locked socket: {e}")
    else:
        log_message("Socket does not exist. Proceeding.")

# Function to start PyDECNET
def start_pydecnet():
    log_message("Starting new PyDECNET process with configuration.")
    command = [PYDECNET_BIN, "--daemon", "--log-config"] + PYDECNET_CONFIG_FILES
    try:
        with open(LOG_INFO_PATH, "w") as info_log, open(LOG_ERROR_PATH, "w") as error_log:
            # Use subprocess.Popen to start the process with redirected logs
            process = subprocess.Popen(
                command,
                stdout=info_log,
                stderr=error_log
            )
        log_message(f"PyDECNET started successfully (PID: {process.pid}).")
    except FileNotFoundError:
        log_message("Failed to start PyDECNET: Executable not found. Please check PYDECNET_BIN path.")
    except Exception as e:
        log_message(f"Failed to start PyDECNET: {e}")

def start_pydecnet_1 ():
    log_message("Starting new PyDECNET process with configuration.")
    command = [PYDECNET_BIN, "--daemon", "--log-config"] + PYDECNET_CONFIG_FILES
    try:
        with open(LOG_INFO_PATH, "w") as info_log, open(LOG_ERROR_PATH, "w") as error_log:
            process = psutil.Popen(command, stdout=info_log, stderr=error_log)
        log_message(f"PyDECNET started successfully (PID: {process.pid}).")
    except Exception as e:
        log_message(f"Failed to start PyDECNET: {e}")

# Function to restart PyDECNET
def restart_pydecnet():
    log_message("Relaunching PyDECNET process.")
    stop_pydecnet()
    remove_locked_socket()
    start_pydecnet()

# Function to update DECNET names
def update_decnet_names():
    log_message("Running DECNET name update script.")
    try:
        subprocess.run([sys.executable, DECNET_NAME_UPDATE_SCRIPT], check=True)
        log_message("DECNET name update completed successfully.")
        # Update the timestamp file
        update_name_update_timestamp()
    except Exception as e:
        log_message(f"Failed to run DECNET name update script: {e}")

def get_last_name_update_time():
    """Get the timestamp of the last name update."""
    try:
        if os.path.exists(NAME_UPDATE_TIMESTAMP_FILE):
            with open(NAME_UPDATE_TIMESTAMP_FILE, 'r') as f:
                timestamp_str = f.read().strip()
                return datetime.fromisoformat(timestamp_str)
    except Exception as e:
        log_message(f"Failed to read name update timestamp: {e}")
    
    # Return epoch time if no timestamp file exists
    return datetime.fromtimestamp(0)

def update_name_update_timestamp():
    """Update the timestamp file with current time."""
    try:
        current_time = datetime.now()
        with open(NAME_UPDATE_TIMESTAMP_FILE, 'w') as f:
            f.write(current_time.isoformat())
        log_message(f"Updated name update timestamp: {current_time}")
    except Exception as e:
        log_message(f"Failed to update name update timestamp: {e}")

def should_update_names():
    """Check if it's time to update DECNET names based on the configured interval."""
    if NAME_UPDATE_INTERVAL <= 0:
        return False  # Automatic updates disabled
    
    last_update = get_last_name_update_time()
    current_time = datetime.now()
    time_since_update = current_time - last_update
    
    # Convert interval from minutes to seconds for comparison
    interval_seconds = NAME_UPDATE_INTERVAL * 60
    
    return time_since_update.total_seconds() >= interval_seconds

def check_and_update_names_if_needed():
    """Check if names need updating and update them if necessary."""
    if should_update_names():
        last_update = get_last_name_update_time()
        hours_since_update = (datetime.now() - last_update).total_seconds() / 3600
        log_message(f"Automatic name update due (last update: {hours_since_update:.1f} hours ago)")
        update_decnet_names()
    else:
        if NAME_UPDATE_INTERVAL > 0:
            last_update = get_last_name_update_time()
            next_update_time = last_update + timedelta(minutes=NAME_UPDATE_INTERVAL)
            time_until_next = next_update_time - datetime.now()
            hours_until_next = time_until_next.total_seconds() / 3600
            if hours_until_next > 0:
                log_message(f"Next automatic name update in {hours_until_next:.1f} hours")

# Function to monitor the DECNET process
def monitor_process():
    while True:
        log_message("Monitoring PyDECNET process.")
        if not any(proc.info['name'] == 'pydecnet' for proc in psutil.process_iter(['name'])):
            log_message("DECNET is off. Restarting!")
            restart_pydecnet()
        else:
            log_message("DECNET process is running.")
        
        check_decnet_link()
        
        # Check if automatic name update is needed
        check_and_update_names_if_needed()
        
        log_message(f"Checking again in {SLEEP_TIME} seconds.")
        time.sleep(SLEEP_TIME)

# Daemon entry point
def daemon_main():
    log_message("Daemon started. Monitoring DECNET.")
    monitor_process()

# Main function to handle command-line arguments
def main():
    # Validate configuration before proceeding
    validate_configuration()
    
    parser = argparse.ArgumentParser(description="DECNET Management Script")
    parser.add_argument("--relaunch", action="store_true", help="Restart the PyDECNET process.")
    parser.add_argument("--update-names", action="store_true", help="Update DECNET node names from HECnet.")
    parser.add_argument("--version", action="store_true", version=DAEMON_VERSION)
    args = parser.parse_args()
    if args.version:
        print(f"HECNET Daemon Version: {DAEMON_VERSION}")
        sys.exit(0)
    if args.relaunch:
        restart_pydecnet()
    elif args.update_names:
        update_decnet_names()
    else:
        # Start the daemon
        with daemon.DaemonContext():
            daemon_main()

if __name__ == "__main__":
    main()
