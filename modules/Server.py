class Server:
    def __init__(self, fqdn, ip_address, description, service_account):
        self.fqdn = fqdn
        self.ip_address = ip_address
        self.description = description
        self.service_account = service_account
        self.services = {}

    def add_service(self, service):
        self.services[service.name] = service

    def __repr__(self):
        return f"Server(fqdn={self.fqdn}, description={self.description})"
