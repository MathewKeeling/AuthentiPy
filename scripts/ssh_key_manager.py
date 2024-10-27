import os
import yaml
import logging
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from tqdm import tqdm
from modules.Environment import install_dir

# Set up logging
log_file = f"{install_dir}/resources/logs/ssh_key_manager.log"
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate SSH key pair if it doesn't exist
def generate_ssh_key():
    print("Checking if SSH key exists...")
    if not os.path.isfile(os.path.expanduser("~/.ssh/id_rsa")):
        print("SSH key not found. Generating new SSH key...")
        os.system("ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa")
        print("SSH key generated.")
    else:
        print("SSH key already exists. Skipping key generation.")

# Function to read server details from YAML file
def read_servers(file_path):
    print(f"Reading server details from {file_path}...")
    with open(file_path, 'r') as file:
        servers = yaml.safe_load(file)
    print("Server details read successfully.")
    return servers

# Function to check if the public key is already on the remote server
def is_key_present(fqdn, service_account):
    try:
        connection = ConnectHandler(
            device_type='linux',
            host=fqdn,
            username=service_account,
            key_file=os.path.expanduser("~/.ssh/id_rsa")
        )
        output = connection.send_command("grep -q '$(cat ~/.ssh/id_rsa.pub)' ~/.ssh/authorized_keys")
        connection.disconnect()
        return output == ''
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        logging.error(f"An error occurred while checking public key on {fqdn}: {e}")
        return False

# Function to copy the public key to each target server
def copy_public_key(servers):
    total_servers = len(servers)
    with tqdm(total=total_servers, desc="Copying public keys", unit="server") as pbar:
        for server, details in servers.items():
            fqdn = details['fqdn']
            service_account = details['service_account']
            if is_key_present(fqdn, service_account):
                logging.info(f"Public key already present on {fqdn}")
            else:
                try:
                    connection = ConnectHandler(
                        device_type='linux',
                        host=fqdn,
                        username=service_account,
                        key_file=os.path.expanduser("~/.ssh/id_rsa")
                    )
                    connection.send_command("mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys", expect_string=r'#')
                    connection.send_command("$(cat ~/.ssh/id_rsa.pub)", expect_string=r'#')
                    connection.disconnect()
                    logging.info(f"Public key copied to {fqdn} successfully")
                except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
                    logging.error(f"Failed to copy public key to {fqdn}: {e}")
            pbar.update(1)

# Function to verify SSH access to each server
def verify_ssh_access(servers):
    total_servers = len(servers)
    with tqdm(total=total_servers, desc="Verifying SSH access", unit="server") as pbar:
        for server, details in servers.items():
            fqdn = details['fqdn']
            service_account = details['service_account']
            try:
                connection = ConnectHandler(
                    device_type='linux',
                    host=fqdn,
                    username=service_account,
                    key_file=os.path.expanduser("~/.ssh/id_rsa")
                )
                output = connection.send_command(f"echo 'SSH to {fqdn} successful'")
                connection.disconnect()
                if "SSH to" in output:
                    logging.info(f"SSH to {fqdn} successful")
                else:
                    logging.error(f"SSH to {fqdn} failed")
            except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
                logging.error(f"SSH to {fqdn} failed: {e}")
            pbar.update(1)

# Main script execution
if __name__ == "__main__":
    servers_file = "./resources/etc/servers.yaml"
    
    print("Starting SSH key generation process...")
    generate_ssh_key()
    
    print("Reading server details...")
    servers = read_servers(servers_file)['servers']
    
    print("Copying public keys to servers...")
    copy_public_key(servers)
    
    print("Verifying SSH access to servers...")
    verify_ssh_access(servers)
    print("Process completed.")
