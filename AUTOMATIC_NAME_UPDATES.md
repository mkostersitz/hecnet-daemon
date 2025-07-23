# Automatic Name Update Feature

## Overview
The HECNET daemon now includes automatic DECNET node name updates at configurable intervals (default: 48 hours).

## New Features Added

### 1. Configuration Management
- **Setup Script Enhancement**: Added `prompt_for_name_update_config()` function to setup.py
- **Configurable Interval**: Users can set update interval in hours (default: 48)
- **Disable Option**: Set interval to 0 to disable automatic updates
- **Persistent Storage**: Interval stored in `pyvenv.cfg` as `hecnet_name_update_interval`

### 2. Daemon Functionality
- **Automatic Updates**: Daemon checks for name updates during each monitoring cycle
- **Timestamp Tracking**: Tracks last update time in `hecnet/logs/last_name_update.txt`
- **Smart Scheduling**: Only updates when configured interval has elapsed
- **Logging**: Comprehensive logging of update status and timing

### 3. New Functions in decnet-daemon.py

#### `get_last_name_update_time()`
- Reads timestamp from file
- Returns datetime of last update
- Falls back to epoch time if no file exists

#### `update_name_update_timestamp()`
- Updates timestamp file with current time
- Called after successful name updates

#### `should_update_names()`
- Compares current time with last update + interval
- Returns True if update is due
- Returns False if disabled (interval = 0)

#### `check_and_update_names_if_needed()`
- Main logic function called from monitoring loop
- Checks if update needed and performs it
- Provides status logging about next update time

### 4. Enhanced User Experience
- **Setup Integration**: Name update configuration included in interactive setup
- **Status Display**: Shows current configuration in setup script
- **Clear Logging**: User-friendly messages about update timing
- **Testing Tools**: Test scripts to verify functionality

## Configuration Options

### During Setup
```bash
python setup.py
```
The script will prompt:
```
=== Name Update Configuration ===
The daemon can automatically update DECNET node names from HECnet.
Default interval: 48 hours (2880 minutes)
Enter update interval in hours (default: 48, 0 to disable): 
```

### Available Options
- **Default (48 hours)**: Press Enter or type `48`
- **Custom Interval**: Enter any number of hours (e.g., `24` for daily)
- **Disable**: Enter `0` to disable automatic updates
- **Frequent Updates**: Values less than 1 hour show warning

## How It Works

1. **Initial Setup**: User configures interval during setup
2. **Daemon Start**: Daemon reads configuration and logs update status
3. **Monitoring Loop**: Each monitoring cycle (default 120 seconds) checks if update needed
4. **Update Check**: Compares current time with last update + configured interval
5. **Automatic Update**: If due, runs name update script and updates timestamp
6. **Status Logging**: Provides clear feedback about update timing

## Files Modified

### setup.py
- Added `prompt_for_name_update_config()` function
- Enhanced configuration display to show update interval
- Added validation and warning for very frequent updates

### decnet-daemon.py
- Added `NAME_UPDATE_INTERVAL` configuration variable
- Added timestamp file path: `NAME_UPDATE_TIMESTAMP_FILE`
- Added four new functions for update management
- Enhanced `update_decnet_names()` to update timestamp
- Integrated update check into `monitor_process()` loop
- Added configuration logging in `validate_configuration()`

### README.md
- Updated features list to include automatic name updates
- Added detailed configuration section
- Updated usage section to mention automatic behavior
- Added explanation of timing and configuration options

## Testing

### Test Scripts Created
- **test_name_update.py**: Tests update logic and timing without running daemon
- **test_find_pydecnet.py**: Existing script for PyDECNET discovery testing

### Manual Testing
```bash
# Check current configuration
python test_name_update.py

# Force immediate name update
python decnet-daemon.py --update-names

# Check daemon status with update info
python decnet-status.py
```

## Benefits

1. **Automated Maintenance**: No manual intervention required for name updates
2. **Configurable**: Users can set frequency based on their needs
3. **Efficient**: Only updates when needed, avoiding unnecessary server load
4. **Reliable**: Robust timestamp tracking and error handling
5. **User-Friendly**: Clear configuration and status messages
6. **Flexible**: Can be disabled or reconfigured anytime

## Example Log Output

```
[2025-07-23 10:30:15] Daemon started. Monitoring DECNET.
[2025-07-23 10:30:15] Automatic name updates enabled: every 48.0 hours
[2025-07-23 10:30:15] Monitoring PyDECNET process.
[2025-07-23 10:30:15] DECNET process is running.
[2025-07-23 10:30:15] DECNET link to MIM is up.
[2025-07-23 10:30:15] Next automatic name update in 47.2 hours
[2025-07-23 10:30:15] Checking again in 120 seconds.
```

This enhancement makes the HECNET daemon fully autonomous for node name management while providing complete user control over the update frequency.
