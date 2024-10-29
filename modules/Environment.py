import yaml

# Load configuration from YAML file
with open("./etc/config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Assign variables from the YAML configuration

subdomain = config["certificates"]["subdomain"]
domain = config["certificates"]["domain"]
fqdn = config["certificates"]["fqdn"]
certificates_root_dir = config["certificates"]["root_dir"]
cert_dir_domain = config["certificates"]["domain_dir"]
cert_dir_subdomain = config["certificates"]["subdomain_dir"]
insrt_root = config["directories"]["insrt_root"]
apps_dir = config["directories"]["apps_dir"]

# Example usage
if __name__ == "__main__":
    print(f"subdomain: {subdomain}")
    print(f"domain: {domain}")
    print(f"fqdn: {fqdn}")
    print(f"certificates_root_dir: {certificates_root_dir}")
    print(f"cert_dir_domain: {cert_dir_domain}")
    print(f"cert_dir_subdomain: {cert_dir_subdomain}")
    print(f"insrt_root: {insrt_root}")
    print(f"apps_dir: {apps_dir}")
