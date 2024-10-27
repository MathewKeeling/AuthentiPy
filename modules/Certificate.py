import os, logging
from netmiko import ConnectHandler, ReadTimeout
from modules.Environment import install_dir


class Certificate:
    """
    Represents a certificate with various attributes.

    Attributes:
        fullchain_source_path (str): The source path of the certificate.
        fullchain_dest_path (str): The destination path of the certificate.
        fullchain_dest_name (str): The name of the certificate at the destination.
        private_key_source_path (str): The source path of the certificate key.
        private_key_dest_path (str): The destination path of the certificate key.
        private_key_dest_name (str): The name of the certificate key at the destination.
        cert_reload_command (dict): The command to reload the certificate.
    """

    def __init__(
        self,
        ca_bundle_source_path: str = None,
        ca_bundle_dest_path: str = None,
        cert_source_path: str = None,
        cert_dest_path: str = None,
        fullchain_source_path: str = None,
        fullchain_dest_path: str = None,
        fullchain_dest_name: str = None,
        private_key_source_path: str = None,
        private_key_dest_path: str = None,
        private_key_dest_name: str = None,
        cert_reload_command: dict = None,
    ):
        self.log_file = f"{install_dir}/resources/logs/certificate.log"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.ca_bundle_source_path = ca_bundle_source_path
        self.ca_bundle_dest_path = ca_bundle_dest_path
        self.cert_source_path = cert_source_path
        self.cert_dest_path = cert_dest_path
        self.fullchain_source_path = fullchain_source_path
        self.fullchain_dest_path = fullchain_dest_path
        self.fullchain_dest_name = fullchain_dest_name
        self.private_key_source_path = private_key_source_path
        self.private_key_dest_path = private_key_dest_path
        self.private_key_dest_name = private_key_dest_name
        self.cert_reload_command = cert_reload_command

    def copy_to_server(self, server):
        # Logic to copy the certificate files to the server
        logging.info(
            f"Copying certificate {self.fullchain_dest_name} to {server.fqdn}:{self.fullchain_dest_path}"
        )

        device = {
            "device_type": "linux",
            "host": server.fqdn,
            "username": server.service_account,
            "use_keys": True,
            "key_file": f"/home/{server.service_account}/.ssh/id_rsa",
            "allow_agent": False,
            "verbose": False,  # Set verbose to False
        }

        # Establish the SSH connection using Netmiko
        connection = ConnectHandler(**device)

        # SCP the certificate files to a temporary location on the server
        temp_ca_bundle_path = f"/tmp/{os.path.basename(self.ca_bundle_source_path)}"
        temp_cert_path = f"/tmp/{os.path.basename(self.cert_source_path)}"
        temp_fullchain_path = f"/tmp/{os.path.basename(self.fullchain_source_path)}"
        temp_private_key_path = f"/tmp/{os.path.basename(self.private_key_source_path)}"

        # SCP the certificate files to a temporary location on the server and redirect output to log file
        scp_ca_bundle = f"scp {self.ca_bundle_source_path} {server.service_account}@{server.fqdn}:{temp_ca_bundle_path} >> {self.log_file} 2>&1"
        scp_cert = f"scp {self.cert_source_path} {server.service_account}@{server.fqdn}:{temp_cert_path} >> {self.log_file} 2>&1"
        scp_fullchain = f"scp {self.fullchain_source_path} {server.service_account}@{server.fqdn}:{temp_fullchain_path} >> {self.log_file} 2>&1"
        scp_private_key = f"scp {self.private_key_source_path} {server.service_account}@{server.fqdn}:{temp_private_key_path} >> {self.log_file} 2>&1"
        os.system(scp_ca_bundle)
        os.system(scp_cert)
        os.system(scp_fullchain)
        os.system(scp_private_key)

        # Move the files to the correct location with sudo
        move_ca_bundle_command = (
            f"sudo mv {temp_ca_bundle_path} {self.ca_bundle_dest_path}"
        )
        move_cert_command = f"sudo mv {temp_cert_path} {self.cert_dest_path}"
        move_fullchain_command = (
            f"sudo mv {temp_fullchain_path} {self.fullchain_dest_path}"
        )
        move_private_key_command = (
            f"sudo mv {temp_private_key_path} {self.private_key_dest_path}"
        )

        # Execute
        connection.send_command(move_ca_bundle_command)
        connection.send_command(move_cert_command)
        connection.send_command(move_fullchain_command)
        connection.send_command(move_private_key_command)

        # Set the correct permissions
        chmod_ca_bundle_command = f"sudo chown root:root {self.ca_bundle_dest_path}"
        chmod_cert_command = f"sudo chown root:root {self.cert_dest_path}"
        chmod_fullchain_command = f"sudo chown root:root {self.fullchain_dest_path}"
        chmod_private_command = f"sudo chown root:root {self.private_key_dest_path}"

        # Execute
        connection.send_command(chmod_ca_bundle_command)
        connection.send_command(chmod_cert_command)
        connection.send_command(chmod_fullchain_command)
        connection.send_command(chmod_private_command)

        # Close the connection
        connection.disconnect()



    def reload_service(self, service, server):
        # Logic to reload the service on the server
        logging.info(f"Reloading service {service.name} on {server.fqdn}")

        # Define the device parameters for Netmiko
        device = {
            "device_type": "linux",
            "host": server.fqdn,
            "username": server.service_account,
            "use_keys": True,
            "key_file": f"/home/{server.service_account}/.ssh/id_rsa",
            "allow_agent": False,
        }

        # Establish the SSH connection using Netmiko
        connection = ConnectHandler(**device)

        # Set the working directory and run the command using a shell
        working_directory = service.install_path  # Replace with the actual working directory
        command = f"cd {working_directory} && {service.certificate.cert_reload_command['command']}"
        full_command = f"sudo bash -c '{command}'"

        # Execute the command with increased read_timeout and expect_string
        try:
            output = connection.send_command(full_command, read_timeout=60)
            logging.info(output)
        except ReadTimeout as e:
            logging.info(f"Command timed out: {e}")

        # Close the connection
        connection.disconnect()


    def __repr__(self):
        return f"Certificate(dest_path={self.fullchain_dest_path}, dest_name={self.fullchain_dest_name})"
