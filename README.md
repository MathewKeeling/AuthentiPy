<table>
  <tr>
    <td>
      <pre>
   _____  _________  ______          
  /  _/ |/ / __/ _ \/_  __/__  __ __ 
 _/ //    /\ \/ , _/ / / / _ \/ // / 
/___/_/|_/___/_/|_| /_(_) .__/\_, /  
                       /_/   /___/   
                         v2024.10.29 
"INSRT's Not Simply Remote Transfer" 
      </pre>
    </td>
    <td>
      <img src="./resources/img/INSRT.png" alt="INSRT.py" style="width: 200px; height: auto;">
    </td>
  </tr>
</table>

## Overview

**INSRT.Py** is a Python-based application designed to manage certificate deployments efficiently.

Due to the nature of how the program is structured, this program works with wildcard certificates only. 

I might consider adding greater levels of control to permit regular certificates as well. Forks/PRs welcomed.

### Features

- **Manage Multiple Certificates**: insrt.py can handle certificates for various services such as GitLab, Graylog, NetBox, OpenNMS, and Postfix.
- **Automated Certificate Reload**: Includes commands to reload certificates automatically after updates.

### Configuration

insrt.py uses YAML files to store configuration details, making it easy to manage and update certificate information.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.12 installed.
- Follow the setup guide.

## Usage

Click here for detailed usage instructions.

1. **Clone the repository**:
    ```sh
    git clone https://github.com/MathewKeeling/insrt.py.git
    cd insrt.py
    ```

2. **Set up the virtual environment**:
    ```sh
    python3.12 -m venv venv
    source ./venv/bin/activate
    pip install pipenv
    pipenv lock
    pipenv install
    ```

3. **Run the script**:
    ```sh
    python insrt.py
    ```

## Configuration File Location

- **Servers Configuration**: `$INSTALL_ROOT/insrt/etc/servers.yaml`
- **Server Service Inventory**: `$INSTALL_ROOT/insrt/etc/server_service_inventory.yaml`
- **Service Manager Configuration**: `$INSTALL_ROOT/insrt/etc/service_manager.yaml`

## Supported Platforms

This script supports Linux systems.

## Limitations

- Currently supports only Linux-based systems.
- Requires manual setup of SSH keys and sudoers configuration as per the setup guide.

## Contribution Requirements

### Formatter

This project uses Black.

## License

This project is licensed under the **GNU General Public License, version 3**.
