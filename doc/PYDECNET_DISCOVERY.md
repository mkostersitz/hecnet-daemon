# PyDECNET Binary Discovery Enhancement

## Overview
The HECNET daemon setup script now uses system commands to automatically locate the PyDECNET binary, making installation much more robust and user-friendly.

## Discovery Methods (in order of priority)

### 1. System Commands
The script first tries to locate `pydecnet` using platform-specific system commands:

#### Windows:
- **Primary**: `where pydecnet` - Uses Windows' built-in where command
- **Fallback**: `powershell -Command "Get-Command pydecnet | Select-Object -ExpandProperty Source"` - Uses PowerShell's Get-Command

#### Linux/macOS:
- **Primary**: `which pydecnet` - Uses the which command to find executables in PATH

### 2. Manual Path Search
If system commands fail, the script searches common installation locations:
- `~/hecnet/bin/pydecnet`
- `~/bin/pydecnet`
- `/usr/local/bin/pydecnet`
- `/usr/bin/pydecnet`
- `~/pydecnet/pydecnet`
- `~/DECnet/bin/pydecnet`
- `~/decnet/bin/pydecnet`

### 3. User Input
If automatic discovery fails, the script prompts the user to manually enter the path.

## Advantages

1. **Cross-Platform**: Works on Windows, Linux, and macOS
2. **PATH-Aware**: Finds PyDECNET if it's installed in any directory in the system PATH
3. **Robust**: Multiple fallback methods ensure high success rate
4. **User-Friendly**: Clear feedback about what was found and where
5. **Executable Verification**: Confirms the found file is actually executable

## Usage

The enhanced discovery runs automatically when you execute:
```bash
python setup.py
```

The script will:
1. Try system commands first (fastest and most reliable)
2. Fall back to checking common paths if needed
3. Prompt for manual input only if all automatic methods fail
4. Validate that the found/entered path is executable
5. Store the path in `pyvenv.cfg` for future use

## Example Output

```
=== PyDECNET Configuration ===
Locating PyDECNET binary...
Found PyDECNET at: /usr/local/bin/pydecnet
Use this path? (Y/n): y
✓ PyDECNET binary configured: /usr/local/bin/pydecnet
```

## Testing

You can test the discovery functionality independently using:
```bash
python test_find_pydecnet.py
```

This will show you exactly how the discovery process works on your system.
