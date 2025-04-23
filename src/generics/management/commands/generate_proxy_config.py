import yaml
from django.conf import settings
from django.core.management.base import BaseCommand

from generics.utils import create_dir_if_not_exists
from website.settings import BASE_DIR


class Command(BaseCommand):
    help = "Creates proxy dynamic_config.yaml file"

    def handle(self, *args, **kwargs):
        config_dict = self.generate_config_dict_version()
        create_dir_if_not_exists(f"{BASE_DIR}/dynamic")
        with open(f"{BASE_DIR}/dynamic/dynamic_config.yaml", 'w') as f:
            yaml.dump(config_dict, f)

    @staticmethod
    def generate_config_dict_version() -> dict:
        config = {
            "http": {
                "routers": {
                    "static": {
                        "rule": "PathPrefix(`/static`)",
                        "service": "webapp",
                        "entrypoints": ["https"]
                    },
                    "media": {
                        "rule": "PathPrefix(`/media`)",
                        "service": "webapp",
                        "entrypoints": ["https"]
                    }
                },
                "services": {
                    "webapp": {
                        "loadBalancer": {
                            "servers": [
                                {
                                    "url": "http://webapp:8000"
                                }
                            ]
                        }
                    },
                }
            }
        }
        for domain, project in settings.MULTI_SITE_PATTERNS.items():
            if domain in ('localhost', '127.0.0.1'):
                continue

            domain_yaml_key_name = domain.replace('-', '').replace('_', '')
            config['http']['routers'][domain_yaml_key_name] = {
                "rule": f"Host(`{domain}`)",
                "entrypoints": ["https"],
                "service": "webapp",
                "tls": {
                    "certResolver": "letsencrypt"
                }
            }
        return config
