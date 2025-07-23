# Configuration Management Guide

## Problem
The `pyvenv.cfg` file contains both system-specific paths and sensitive information (like email passwords) that should not be committed to version control, but new users need a starting template.

## Solution
We use a template-based approach that keeps sensitive data local while providing a clean template for new installations.

## File Structure

### `pyvenv.cfg.template` (Tracked by Git)
- Contains only the version number and placeholder values
- Safe to commit to version control
- Used as the basis for new installations

### `pyvenv.cfg` (Ignored by Git)
- Created from template during setup
- Contains actual configuration values
- Listed in `.gitignore` to prevent accidental commits

## How It Works

### 1. Initial Setup
When a new user runs `python setup.py`:
1. Script checks if `pyvenv.cfg` exists
2. If not, automatically copies `pyvenv.cfg.template` to `pyvenv.cfg`
3. Proceeds with interactive configuration
4. Saves real configuration values to `pyvenv.cfg`

### 2. Version Control
- **`pyvenv.cfg.template`**: Committed to Git with safe placeholder values
- **`pyvenv.cfg`**: Ignored by Git (listed in `.gitignore`)
- Users get a clean template but their personal config stays private

### 3. Updates
When you update the project:
1. Update `pyvenv.cfg.template` with new configuration options
2. Commit the template changes
3. Users run `python setup.py` to get prompted for new settings
4. Their existing settings are preserved, new ones are added

## Template Content

```properties
# Python Virtual Environment Configuration Template
# Copy this file to 'pyvenv.cfg' and configure for your system
# Run 'python setup.py' to automatically configure all settings

# HECNET Daemon Version
hecnet_daemon_version = 1.0

# Standard Python Virtual Environment Settings (will be auto-configured)
home = /usr/bin
include-system-site-packages = false
version = 3.11.2
executable = /usr/bin/python3.11
command = /path/to/your/python3 -m venv /path/to/your/hecnet

# HECNET Daemon Configuration (configured by setup.py)
# hecnet_sender_email = your-email@gmail.com
# hecnet_sender_password = your-app-password
# hecnet_receiver_email = recipient@example.com
# hecnet_target_host = MIM
# hecnet_pydecnet_bin = /path/to/pydecnet
# hecnet_name_update_interval = 2880
```

## Benefits

1. **Security**: No sensitive data in version control
2. **Usability**: New users get automatic template setup  
3. **Maintainability**: Easy to add new configuration options
4. **Flexibility**: Users can manually edit template if needed
5. **Robustness**: Setup script handles missing files gracefully

## Manual Process (if needed)

If automatic setup fails, users can manually:
```bash
# Copy template to active config
cp pyvenv.cfg.template pyvenv.cfg

# Run setup to configure
python setup.py
```

## Adding New Configuration Options

1. Add the new option to `pyvenv.cfg.template` as a commented placeholder
2. Update `setup.py` to prompt for the new option
3. Update `decnet-daemon.py` to read the new option
4. Document the new option in README.md

The template approach ensures that your personal configuration never gets uploaded to GitHub while making the project easy to set up for new users.
