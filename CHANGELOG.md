# Changelog

## [2024.10.26] - 2024-10-26

### Added
- Initial release of `insrt.py` and `ssh_key_manager.py`.
- `insrt.py`:
  - Script to automatically update certificates on systems.
  - Logging setup to `$INSTALL_ROOT/insrt/resources/logs/insrt.log`.
  - Server and service management using `ServerManager` and `ServiceManager`.
  - Certificate update process with progress tracking using `tqdm`.
- `ssh_key_manager.py`:
  - SSH key generation if not present.
  - Reading server details from YAML.
  - Checking and copying public keys to remote servers.
  - Verifying SSH access to servers.
  - Logging setup to `$INSTALL_ROOT/resources/logs/ssh_key_manager.log`.

## [2024.10.29] - 2024-10-29

### Added
- Initial setup for changelog in calver format.
- `pytest-mock==3.8.0` to Pipfile.
- New logging configuration file.
- "Contribution Requirements" section in README specifying the use of Black formatter.
- "License" section in README.
- Tests for `ssh_key_manager.py`.

### Updated
- Paths in README under "Configuration File Location".
- Paths in `certificate.py` and `certificatemanager.py`.

### Removed
- `os`, `logging`, `ConnectHandler`, `ReadTimeout`, and `install_dir` imports from `certificate.py`.
- Logging setup and `install_dir` usage in `certificate.py`.

### Refactored
- `environment.py`, `serverManager.py`, `certificateManager.py`, and `certificates.py`.
- `ssh_key_manager.py` to ensure functionality.
