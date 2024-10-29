from modules.Environment import subdomain, fqdn, domain
from modules.Certificate import Certificate
from modules.Environment import (
    certificates_root_dir,
    apps_dir,
    cert_dir_subdomain,
)


class CertificateManager:
    """
    Manages multiple certificates.

    Attributes:
        gitlab (Certificate): GitLab certificate.
        graylog (Certificate): Graylog certificate.
        netbox (Certificate): NetBox certificate.
        opennms (Certificate): OpenNMS certificate.
        postfix (Certificate): Postfix certificate.
    """

    def __init__(self):
        self.subdomain = subdomain
        self.domain = domain
        self.fqdn = fqdn

        self.gitlab = self.create_certificate("gitlab")
        self.graylog = self.create_certificate("graylog")
        self.netbox = self.create_certificate("netbox")
        self.opennms = self.create_certificate("opennms")
        self.openvpn = self.create_openvpn_certificate()
        self.planka = self.create_certificate("planka")
        self.postfix = self.create_postfix_certificate()

    def create_certificate(self, app_name: str):
        return Certificate(
            ca_bundle_source_path=f"{cert_dir_subdomain}/ca.cer",
            ca_bundle_dest_path=f"{apps_dir}/{app_name}/volumes/caddy/cert.crt",
            cert_source_path=f"{cert_dir_subdomain}/{self.fqdn}.cer",
            cert_dest_path=f"{apps_dir}/{app_name}/volumes/caddy/{self.fqdn}.cer",
            fullchain_source_path=f"{cert_dir_subdomain}/fullchain.cer",
            fullchain_dest_path=f"{apps_dir}/{app_name}/volumes/caddy/cert.crt",
            fullchain_dest_name="cert.crt",
            private_key_source_path=f"{cert_dir_subdomain}/{self.fqdn}.key",
            private_key_dest_path=f"{apps_dir}/{app_name}/volumes/caddy/key.key",
            private_key_dest_name="key.key",
            cert_reload_command={
                "user": "root",
                "command": f"docker compose restart tls > /dev/null 2>&1",
            },
        )

    def create_openvpn_certificate(self):
        return Certificate(
            ca_bundle_source_path=f"{certificates_root_dir}/{self.domain}_ecc/{self.domain}_ecc/ca.cer",
            ca_bundle_dest_path=f"/etc/webcerts/vpn.{self.domain}/ca.cer",
            cert_source_path=f"{certificates_root_dir}/{self.domain}_ecc/{self.domain}_ecc/{self.domain}.cer",
            cert_dest_path=f"/etc/webcerts/vpn.{self.domain}/{self.domain}.cer",
            fullchain_source_path=f"{certificates_root_dir}/{self.domain}_ecc/{self.domain}_ecc/fullchain.cer",
            fullchain_dest_path=f"/etc/webcerts/vpn.{self.domain}/fullchain.cer",
            fullchain_dest_name="fullchain.cer",
            private_key_source_path=f"{certificates_root_dir}/{self.domain}_ecc/{self.domain}_ecc/{self.domain}.key",
            private_key_dest_path=f"/etc/webcerts/vpn.{self.domain}/{self.domain}.key",
            private_key_dest_name="{self.domain}.key",
            cert_reload_command={
                "user": "root",
                "command": f'mkdir -p /etc/webcerts/vpn.{self.domain}; cd /usr/local/openvpn_as/scripts/; ./sacli --key "cs.priv_key" --value_file "/etc/webcerts/vpn.{self.domain}/{self.domain}.key" ConfigPut; ./sacli --key "cs.cert" --value_file "/etc/webcerts/vpn.{self.domain}/{self.domain}.cer" ConfigPut; ./sacli --key "cs.ca_bundle" --value_file "/etc/webcerts/vpn.{self.domain}/ca.cer" ConfigPut; ./sacli start',
            },
        )

    def create_postfix_certificate(self):
        return Certificate(
            ca_bundle_source_path=f"{cert_dir_subdomain}/ca.cer",
            ca_bundle_dest_path="/etc/postfx/certificates/cert.crt",
            cert_source_path=f"{cert_dir_subdomain}/{self.fqdn}.cer",
            cert_dest_path="/etc/postfx/certificates/{self.fqdn}.cer",
            fullchain_source_path=f"{cert_dir_subdomain}/fullchain.cer",
            fullchain_dest_path="/etc/postfx/certificates/postfix.cer",
            fullchain_dest_name="postfix.cer",
            private_key_source_path=f"{cert_dir_subdomain}/{self.fqdn}.key",
            private_key_dest_path="/etc/postfx/certificates/postfix.key",
            private_key_dest_name="postfix.key",
            cert_reload_command={
                "user": "root",
                "command": "postfix reload; systemctl restart postfix",
            },
        )
