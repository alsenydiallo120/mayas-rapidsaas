import json
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = "Creates a new Django app with additional setup for HTML templates"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="The name of the app to create")

    def handle(self, *args, **kwargs):
        app_name = kwargs["app_name"]

        # Exécute la commande standard `startapp`
        try:
            call_command("startapp", app_name, template="static/app_tmpl", extension=["html", "py", "js"])
        except CommandError as e:
            self.stderr.write(self.style.ERROR(f"Error creating app: {e}"))
            return

        # Dossier de l'application nouvellement créée
        app_directory = os.path.join(settings.BASE_DIR, app_name)
        static_directory = os.path.join(settings.BASE_DIR, "static")

        # Effectue le remplacement de {{ app_name }} dans les fichiers HTML
        self.replace_app_name_in_html_files(app_name, app_directory)
        self.create_template_css_output_file(app_name, static_directory)
        self.add_command_to_package_json(app_name)
        self.stdout.write(self.style.SUCCESS(f"Successfully created app '{app_name}'"))

    @staticmethod
    def replace_app_name_in_html_files(app_name, app_directory):
        for root, _, files in os.walk(app_directory):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        content = f.read()
                    # Remplacement de `{{ app_name }}`
                    content = content.replace("{{ app_name }}", app_name)
                    with open(file_path, "w") as f:
                        f.write(content)

    @staticmethod
    def create_template_css_output_file(app_name, static_directory):
        with open(f"{static_directory}/src/output_template.css", 'r') as f:
            css_template_content = f.read()

        with open(f"{static_directory}/src/output_{app_name}.css", 'w') as f:
            f.write(css_template_content)

    @staticmethod
    def add_command_to_package_json(app_name):
        with open(settings.BASE_DIR.parent / "package.json", "r") as f:
            package_json = json.load(f)

        package_json['scripts'][f'tw-watch-{app_name.replace("_", "-")}'] = f"npx tailwindcss -c ./src/{app_name}/theme.js -i ./src/static/src/input.css -o ./src/static/src/output_{app_name}.css --watch"

        with open(settings.BASE_DIR.parent / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
