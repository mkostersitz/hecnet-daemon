# Contributing to HECNET Daemon

Thank you for your interest in contributing to the HECNET Daemon project! This guide will help you get started.

## Project Overview

The HECNET Daemon is a Python-based monitoring system for PyDECNET routers, designed to provide reliable remote monitoring and automatic maintenance for DECNET nodes on the HECnet (Historic Ethernet Computer Network).

## Ways to Contribute

### 1. Bug Reports
- Use the GitHub Issues tracker
- Include detailed steps to reproduce
- Provide system information (OS, Python version, PyDECNET version)
- Include relevant log files from `hecnet/logs/`

### 2. Feature Requests
- Check existing issues first to avoid duplicates
- Clearly describe the use case and expected behavior
- Consider backward compatibility implications

### 3. Code Contributions
- Fork the repository
- Create a feature branch from `main`
- Follow the coding standards below
- Include tests for new functionality
- Update documentation as needed

### 4. Documentation Improvements
- Fix typos, improve clarity
- Add examples and use cases
- Update installation guides
- Improve troubleshooting sections

## Development Setup

### Prerequisites
- Python 3.6 or higher
- PyDECNET installed and configured
- Git for version control

### Local Development
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/hecnet-daemon.git
cd hecnet-daemon

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy configuration template
cp pyvenv.cfg.template pyvenv.cfg

# Configure for your system
python setup.py
```

### Testing Your Changes
```bash
# Test basic functionality
python decnet-status.py

# Test daemon restart
python decnet-daemon.py --relaunch

# Test name updates
python decnet-daemon.py --update-names

# Test PyDECNET discovery
python test_find_pydecnet.py
```

## Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Include docstrings for functions and classes
- Keep functions focused and single-purpose

### Code Organization
- **decnet-daemon.py**: Main daemon functionality
- **setup.py**: Configuration and setup logic
- **decnet-status.py**: Status monitoring and reporting
- **decnet-name-update.py**: HECnet node name management

### Error Handling
- Use try/catch blocks for external dependencies
- Log errors with descriptive messages
- Provide user-friendly error messages
- Include recovery suggestions where possible

### Configuration
- Use the `pyvenv.cfg` system for user settings
- For system variables not containing personally identifiable data (PII) add them to the template, **never upload your own pyenv.cfg**
- Provide sensible defaults
- Validate configuration on startup
- Support cross-platform paths

## Pull Request Process

### Before Submitting
1. **Test thoroughly** on your target platform and if possible on every other platform.
2. **Update documentation** if you've changed functionality
3. **Add comments** explaining complex logic
4. **Check compatibility** with different Python versions
5. **Verify configuration security** (no sensitive data in code)

### Pull Request Guidelines
1. **Clear title** describing the change
2. **Detailed description** of what and why
3. **Link related issues** using GitHub keywords
4. **Include test results** from your environment
5. **Request specific reviewers** if needed

### Example PR Description
```
## Summary
Add support for custom SMTP servers beyond Gmail

## Changes
- Modified `send_email()` function to accept server/port parameters
- Updated `setup.py` to prompt for SMTP configuration
- Added validation for SMTP settings
- Updated documentation with new configuration options

## Testing
- Tested with Gmail (existing functionality)
- Tested with custom SMTP server
- Verified error handling for invalid configurations

## Related Issues
Closes #123
```

## Specific Contribution Areas

### 1. Platform Support
**Windows Support**: Help improve Windows compatibility
- PowerShell integration
- Windows service installation
- Path handling improvements

**macOS Support**: Enhance macOS experience
- LaunchAgent improvements
- Better path detection
- Native notifications

### 2. Email Notifications
**SMTP Providers**: Support for additional email providers
- Microsoft 365/Outlook
- Custom SMTP servers
- Alternative notification methods (Slack, Discord, etc.)

**Message Templates**: Improve notification content
- HTML email templates
- Configurable message formats
- Severity levels

### 3. Monitoring Features
**Additional Metrics**: Expand monitoring capabilities
- Network latency monitoring
- Resource usage tracking
- Historical data collection

**Alerting Logic**: Improve notification intelligence
- Rate limiting
- Alert escalation
- Maintenance windows

### 4. Configuration Management
**GUI Configuration**: Web-based or desktop configuration interface
**Configuration Validation**: Better error checking and suggestions
**Migration Tools**: Help users upgrade configurations

### 5. Documentation
**Video Tutorials**: Screen recordings of setup process
**Platform-Specific Guides**: Detailed OS-specific instructions
**Troubleshooting Database**: Common issues and solutions

## Code Review Criteria

### Functionality
- Does the code work as intended?
- Are edge cases handled appropriately?
- Is error handling comprehensive?

### Quality
- Is the code readable and maintainable?
- Are there adequate comments and documentation?
- Does it follow project conventions?

### Security
- Are user credentials handled securely?
- Is input validation sufficient?
- Are file permissions appropriate?

### Compatibility
- Does it work on target platforms?
- Is it compatible with different Python versions?
- Does it integrate well with existing features?

## Release Process

### Version Numbering
We use semantic versioning (SemVer):
- **Major** (1.0.0): Breaking changes
- **Minor** (1.1.0): New features, backward compatible
- **Patch** (1.1.1): Bug fixes, backward compatible

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number incremented in `pyvenv.cfg.template`
- [ ] Release notes prepared
- [ ] Tagged in Git

## Getting Help

### Questions
- Check existing documentation first
- Search closed issues for similar questions
- Ask in GitHub Discussions or Issues

### Development Issues
- Include your development environment details
- Provide steps you've already tried
- Share relevant code snippets

### Contact
- GitHub Issues: Primary communication channel
- Project maintainer: [@mkostersitz](https://github.com/mkostersitz)

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- README.md acknowledgments section

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project. See [LICENSE](LICENSE) for details.

---

Thank you for helping make HECNET Daemon better for the entire HECnet community! 🚀
