import os
import logging
import logging.config
import subprocess
from netmiko import ConnectHandler, ReadTimeout
from modules.Environment import insrt_root

# Load logging configuration
logging.config.fileConfig("./etc/logging.conf")
logger = logging.getLogger("insrt")


class Certificate:
    def __init__(
        self,
        ca_bundle_source_path=None,
        ca_bundle_dest_path=None,
        cert_source_path=None,
        cert_dest_path=None,
        fullchain_source_path=None,
        fullchain_dest_path=None,
        fullchain_dest_name=None,
        private_key_source_path=None,
        private_key_dest_path=None,
        private_key_dest_name=None,
        cert_reload_command=None,
    ):
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
        logger.info(
            f"Copying certificate {self.fullchain_dest_name} to {server.fqdn}:{self.fullchain_dest_path}"
        )
        device = {
            "device_type": "linux",
            "host": server.fqdn,
            "username": server.service_account,
            "use_keys": True,
            "key_file": f"/home/{server.service_account}/.ssh/id_rsa",
            "allow_agent": False,
            "verbose": False,
        }
        connection = ConnectHandler(**device)

        paths = {
            "ca_bundle": (self.ca_bundle_source_path, self.ca_bundle_dest_path),
            "cert": (self.cert_source_path, self.cert_dest_path),
            "fullchain": (self.fullchain_source_path, self.fullchain_dest_path),
            "private_key": (self.private_key_source_path, self.private_key_dest_path),
        }

        for key, (src, dest) in paths.items():
            temp_path = f"/tmp/{os.path.basename(src)}"
            logger.info(
                f"Copying {src} to {server.service_account}@{server.fqdn}:{temp_path}"
            )
            result = subprocess.run(
                ["scp", src, f"{server.service_account}@{server.fqdn}:{temp_path}"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                logger.info(f"Successfully copied {src} to {temp_path}")
            else:
                logger.error(f"Failed to copy {src} to {temp_path}: {result.stderr}")

            connection.send_command(f"sudo mv {temp_path} {dest}")
            connection.send_command(f"sudo chown root:root {dest}")

        connection.disconnect()

    def reload_service(self, service, server):
        logger.info(f"Reloading service {service.name} on {server.fqdn}")
        device = {
            "device_type": "linux",
            "host": server.fqdn,
            "username": server.service_account,
            "use_keys": True,
            "key_file": f"/home/{server.service_account}/.ssh/id_rsa",
            "allow_agent": False,
        }
        connection = ConnectHandler(**device)
        command = f"cd {service.install_path} && {service.certificate.cert_reload_command['command']}"
        try:
            output = connection.send_command(
                f"sudo bash -c '{command}'", read_timeout=60
            )
            logger.info(output)
        except ReadTimeout as e:
            logger.info(f"Command timed out: {e}")
        connection.disconnect()

    def __repr__(self):
        return f"Certificate(dest_path={self.fullchain_dest_path}, dest_name={self.fullchain_dest_name})"
