# Setup Instructions

## Setup Instructions

1. [Setup Virtual Environment](/resources/docs/setup/virtualenv.md)

1. Configure all etc files [here](/resources/etc)

    1. [Populate AND rename your ```config.yaml``` file](/resources/etc/config_template.yaml)

    1. [Populate AND rename your ```server_service_inventory.yaml``` file](/resources/etc/server_service_inventory_template.yaml)

    1. [Populate AND rename your ```servers.yaml``` file](/resources/etc/servers_template.yaml)

    1. [Populate AND rename your ```service_manager.yaml``` file](/resources/etc/service_manager_template.yaml)

1. Propagate SSH Keys

    ```bash
    . ./scripts/ssh_key_manager.sh
    ```

1. [Ensure sudoers file is up to date](/resources/docs/setup/sudoers.md)