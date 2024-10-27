"""
insrt.Py
2024.10.26

Overview:
    This script will automatically go out to your systems and update their certificates with the latest certificate.

Dependencies:
    /resources/docs/setup_virtual_environment.md
    /resources/docs/setup/ssh_keys.md
    /resources/docs/setup/sudoers.md
"""

import os
import yaml
import logging
from tqdm import tqdm
from modules.ServerManager import ServerManager, Server
from modules.ServiceManager import ServiceManager
from modules.Environment import install_dir

# Set up logging
log_file = f"{install_dir}/resources/logs/insrt.log"
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Gather servers
servers_config_dir = f"{install_dir}/resources/etc/servers.yaml"
servers = ServerManager(config_file=servers_config_dir)

# Load server_service_inventory from YAML file
with open(f"{install_dir}/resources/etc/server_service_inventory.yaml", "r") as file:
    server_service_inventory = yaml.safe_load(file)

# Load services configuration from YAML file
with open(f"{install_dir}/resources/etc/service_manager.yaml", "r") as file:
    service_manager_yaml = yaml.safe_load(file)

# Initialize ServiceManager with services from YAML
service_manager = ServiceManager(services_config=service_manager_yaml)

# Adding services to servers using a loop
for server in server_service_inventory['server_service_inventory']:
    server_name = server['name']
    service_name = server['service']
    server_obj = getattr(servers, server_name)
    service_obj = getattr(service_manager, service_name)
    server_obj.add_service(service_obj)

def update_certificates():
    """
    Iterates over servers and updates certificates.
    """
    total_servers = len(vars(servers))
    with tqdm(total=total_servers, desc="Updating certificates", unit="server") as pbar:
        for server_name, server in vars(servers).items():
            if isinstance(server, Server):  # Ensure we are dealing with Server instances
                for service_name, service in server.services.items():
                    if service.certificate:
                        logging.info(f"Updating certificate for {server.fqdn} - Service: {service_name}")
                        service.certificate.copy_to_server(server=server)
                        logging.info(f"Certificate copied to {server.fqdn}")
                        service.certificate.reload_service(service=service, server=server)
                        logging.info(f"Service {service_name} restarted on {server.fqdn}")
            pbar.update(1)

def main():
    update_certificates()

if __name__ == "__main__":
    for server_name, server in vars(servers).items():
        service_counter = 0
        logging.info(f"\nServer FQDN: {server.fqdn}")
        logging.info(f"Server IP: {server.ip_address}")
        logging.info(f"Server Description: {server.description}")
        for service_name, service in server.services.items():
            service_counter += 1
            logging.info(f"Service {service_counter} Name: {service.name}")
            logging.info(f"Service {service_counter} Ports: {service.ports}")
    main()
