import yaml

# Load configuration from YAML file
with open('./resources/etc/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Assign variables from the YAML configuration

subdomain = config['certificates']['subdomain']
domain = config['certificates']['domain']
fqdn = config['certificates']['fqdn']
certificates_root_dir = config['certificates']['root_dir']
cert_dir_domain = config['certificates']['domain_dir']
cert_dir_subdomain = config['certificates']['subdomain_dir']
install_dir = config['directories']['install_dir']
source_apps_dir = config['directories']['source_apps']

# Example usage
if __name__ == "__main__":
    print(f"subdomain: {subdomain}")
    print(f"domain: {domain}")
    print(f"fqdn: {fqdn}")
    print(f"certificates_root_dir: {certificates_root_dir}")
    print(f"cert_dir_domain: {cert_dir_domain}")
    print(f"cert_dir_subdomain: {cert_dir_subdomain}")
    print(f"install_dir: {install_dir}")
    print(f"source_apps_dir: {source_apps_dir}")
