class Service:
    """
    Represents a service with various attributes.

    Attributes:
        ports (dict[int, str]): A dictionary mapping port numbers to descriptions.
        name (str): The name of the service.
        description (str): A brief description of the service.
        install_path (str): The installation path of the service.
        cert_req (bool): Indicates if a certificate is required.
        certificate (str, optional): The certificate for the service, if required.

    Raises:
        ValueError: If cert_req is True and certificate is not provided.
    """

    def __init__(
        self,
        ports: dict[int, str],
        name: str,
        description: str,
        install_path: str,
        cert_req: bool,
        certificate: str = None,
    ):
        self.ports = ports
        self.name = name
        self.description = description
        self.install_path = install_path
        self.cert_req = cert_req
        self.certificate = certificate

        if self.cert_req and not self.certificate:
            raise ValueError("Certificate is required when cert_req is True")

    def __repr__(self):
        return f"Service(name={self.name}, ports={self.ports})"
