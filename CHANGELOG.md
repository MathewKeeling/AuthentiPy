# Changelog

## [2024.10.26] - 2024-10-26

### Added
- Initial release of `authentipy.py` and `ssh_key_manager.py`.
- `authentipy.py`:
  - Script to automatically update certificates on systems.
  - Logging setup to `$INSTALL_ROOT/authentipy/resources/logs/authentipy.log`.
  - Server and service management using `ServerManager` and `ServiceManager`.
  - Certificate update process with progress tracking using `tqdm`.
- `ssh_key_manager.py`:
  - SSH key generation if not present.
  - Reading server details from YAML.
  - Checking and copying public keys to remote servers.
  - Verifying SSH access to servers.
  - Logging setup to `$INSTALL_ROOT/resources/logs/ssh_key_manager.log`.
