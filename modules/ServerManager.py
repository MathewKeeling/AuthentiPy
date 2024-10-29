import os
import yaml
from modules.Server import Server


class ServerManager:
    """
    Manages multiple servers.
    """

    def __init__(self, config_file="servers.yaml"):
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)

        for server_name, server_info in config["servers"].items():
            setattr(self, server_name, Server(**server_info))


def main():
    servers = ServerManager(config_dir="/path/to/your/yaml/directory")
    print(servers)


if __name__ == "__main__":
    main()
