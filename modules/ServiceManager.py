from modules.Service import Service
from modules.CertificateManager import CertificateManager

class ServiceManager:
    """
    Manages multiple services.

    Attributes:
        services (dict): Dictionary of services.
    """

    def __init__(self, services_config: dict):
        self.services = {}

        for service_name, service_info in services_config['services'].items():
            certificate = None
            if service_info.get('cert_req'):
                certificate = getattr(CertificateManager(), service_info['certificate'])

            self.services[service_name] = Service(
                ports=service_info['ports'],
                name=service_info['name'],
                description=service_info['description'],
                install_path=service_info['install_path'],
                cert_req=service_info['cert_req'],
                certificate=certificate
            )

    def __getattr__(self, item):
        return self.services.get(item)
