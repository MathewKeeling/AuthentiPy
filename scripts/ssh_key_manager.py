import os
import yaml
import logging
import logging.config
from tqdm import tqdm
from modules.Environment import insrt_root

# Load logging configuration
logging.config.fileConfig("./etc/logging.conf")
logger = logging.getLogger("ssh_key_manager")


def generate_ssh_key():
    if not os.path.isfile(os.path.expanduser("~/.ssh/id_rsa")):
        os.system("ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa")


def read_servers(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def copy_public_key(servers):
    with tqdm(total=len(servers), desc="Copying public keys", unit="server") as pbar:
        for server, details in servers.items():
            fqdn, service_account = details["fqdn"], details["service_account"]
            # Prompt for password and copy the public key to the remote server
            os.system(f"ssh-copy-id -i ~/.ssh/id_rsa.pub {service_account}@{fqdn}")
            logger.info(f"Key copied to {fqdn}")
            pbar.update(1)


def verify_ssh_access(servers):
    with tqdm(total=len(servers), desc="Verifying SSH access", unit="server") as pbar:
        for server, details in servers.items():
            fqdn, service_account = details["fqdn"], details["service_account"]
            # Verify SSH access and log the current user and hostname from the remote server
            command = f"ssh -o BatchMode=yes {service_account}@{fqdn} 'echo $(whoami)@$(hostname)'"
            result = os.popen(command).read().strip()
            if result:
                logger.info(f"SSH to {fqdn} successful. User and hostname: {result}")
            else:
                logger.error(f"SSH to {fqdn} failed")
            pbar.update(1)


if __name__ == "__main__":
    servers_file = f"{insrt_root}/etc/servers.yaml"
    generate_ssh_key()
    servers = read_servers(servers_file)["servers"]
    copy_public_key(servers)
    verify_ssh_access(servers)
    print("Process completed.")
