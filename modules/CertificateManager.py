from modules.Environment import subdomain, fqdn, domain
from modules.Certificate import Certificate
from modules.Environment import (
    certificates_root_dir,
    source_apps_dir
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
        self.fqdn = f"{self.subdomain}.{self.domain}"

        self.gitlab = Certificate(
            ca_bundle_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/ca.cer",
            ca_bundle_dest_path=f"{source_apps_dir}/gitlab/volumes/caddy/cert.crt",
            cert_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.cer",
            cert_dest_path=f"{source_apps_dir}/gitlab/volumes/caddy/{self.fqdn}.cer",
            fullchain_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/fullchain.cer",
            fullchain_dest_path=f"{source_apps_dir}/gitlab/volumes/caddy/cert.crt",
            fullchain_dest_name="cert.crt",
            private_key_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.key",
            private_key_dest_path=f"{source_apps_dir}/gitlab/volumes/caddy/key.key",
            private_key_dest_name="key.key",
            cert_reload_command={
                "user": "root",
                "command": f"docker compose restart tls > /dev/null 2>&1",  # old version of docker compose, needs upgraded
            },
        )

        self.graylog = Certificate(
            ca_bundle_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/ca.cer",
            ca_bundle_dest_path=f"{source_apps_dir}/graylog/volumes/caddy/cert.crt",
            cert_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.cer",
            cert_dest_path=f"{source_apps_dir}/graylog/volumes/caddy/{self.fqdn}.cer",
            fullchain_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/fullchain.cer",
            fullchain_dest_path=f"{source_apps_dir}/graylog/volumes/caddy/cert.crt",
            fullchain_dest_name="cert.crt",
            private_key_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.key",
            private_key_dest_path=f"{source_apps_dir}/graylog/volumes/caddy/key.key",
            private_key_dest_name="key.key",
            cert_reload_command={
                "user": "root",
                "command": f"docker compose restart tls > /dev/null 2>&1",
            },
        )

        self.netbox = Certificate(
            ca_bundle_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/ca.cer",
            ca_bundle_dest_path=f"{source_apps_dir}/netbox/volumes/caddy/cert.crt",
            cert_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.cer",
            cert_dest_path=f"{source_apps_dir}/netbox/volumes/caddy/{self.fqdn}.cer",
            fullchain_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/fullchain.cer",
            fullchain_dest_path=f"{source_apps_dir}/netbox/volumes/caddy/cert.crt",
            fullchain_dest_name="cert.crt",
            private_key_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.key",
            private_key_dest_path=f"{source_apps_dir}/netbox/volumes/caddy/key.key",
            private_key_dest_name="key.key",
            cert_reload_command={
                "user": "root",
                "command": f"docker compose restart tls > /dev/null 2>&1",
            },
        )

        self.opennms = Certificate(
            ca_bundle_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/ca.cer",
            ca_bundle_dest_path=f"{source_apps_dir}/opennms/volumes/caddy/cert.crt",
            cert_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.cer",
            cert_dest_path=f"{source_apps_dir}/opennms/volumes/caddy/{self.fqdn}.cer",
            fullchain_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/fullchain.cer",
            fullchain_dest_path=f"{source_apps_dir}/opennms/volumes/caddy/cert.crt",
            fullchain_dest_name="cert.crt",
            private_key_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.key",
            private_key_dest_path=f"{source_apps_dir}/opennms/volumes/caddy/key.key",
            private_key_dest_name="key.key",
            cert_reload_command={
                "user": "root",
                "command": f"docker compose restart tls > /dev/null 2>&1",
            },
        )

        self.openvpn = Certificate(
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

        self.planka = Certificate(
            ca_bundle_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/ca.cer",
            ca_bundle_dest_path=f"{source_apps_dir}/planka/volumes/caddy/cert.crt",
            cert_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.cer",
            cert_dest_path=f"{source_apps_dir}/planka/volumes/caddy/{self.fqdn}.cer",
            fullchain_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/fullchain.cer",
            fullchain_dest_path=f"{source_apps_dir}/planka/volumes/caddy/cert.crt",
            fullchain_dest_name="cert.crt",
            private_key_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.key",
            private_key_dest_path=f"{source_apps_dir}/planka/volumes/caddy/key.key",
            private_key_dest_name="key.key",
            cert_reload_command={
                "user": "root",
                "command": f"docker compose restart tls > /dev/null 2>&1",
            },
        )

        self.postfix = Certificate(
            ca_bundle_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/ca.cer",
            ca_bundle_dest_path="/etc/postfx/certificates/cert.crt",
            cert_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.cer",
            cert_dest_path="/etc/postfx/certificates/{self.fqdn}.cer",
            fullchain_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/fullchain.cer",
            fullchain_dest_path="/etc/postfx/certificates/postfix.cer",
            fullchain_dest_name="postfix.cer",
            private_key_source_path=f"{certificates_root_dir}/{self.fqdn}_ecc/{self.fqdn}_ecc/{self.fqdn}.key",
            private_key_dest_path="/etc/postfx/certificates/postfix.key",
            private_key_dest_name="postfix.key",
            cert_reload_command={
                "user": "root",
                "command": "postfix reload; systemctl restart postfix",
            },
        )
