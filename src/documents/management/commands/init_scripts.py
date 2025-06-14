import os
import subprocess
from django.core import management
from django.core.management.base import BaseCommand

SCRIPTS_FOLDER = "/app/scripts"
SCRIPTS_TO_RUN = ["init_form_base_line_configs.py"]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("migrate", verbosity=2, interactive=False)

        for script in SCRIPTS_TO_RUN:
            script_path = f"{SCRIPTS_FOLDER}/{script}"
            self.stdout.write(f"Running script: {script_path}")
            
            env = os.environ.copy()
            env["PYTHONPATH"] = "/app/src"

            result = subprocess.run(["python", script_path], env=env)
            if result.returncode != 0:
                self.stderr.write(f"Script {script} failed")
