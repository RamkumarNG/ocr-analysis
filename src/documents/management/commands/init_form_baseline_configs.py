from django.core.management.base import BaseCommand
from django.db import transaction
from configs.models import FormBaseline


CONFIG_DATA = [
    {
        "file_type": "itr",
        "base_font_names": ["Times-Bold", "Times-Roman"],
        "base_font_size": [8.0],
    }
]

class Command(BaseCommand):
    help = "Initialize form baseline configs"

    def handle(self, *args, **options):
        self.stdout.write("Starting form baseline config initialization...")
        self.run_config_init()
        self.stdout.write(self.style.SUCCESS("✅ Form baseline config initialization complete."))

    @transaction.atomic
    def run_config_init(self):
        for config in CONFIG_DATA:
            form_obj, created = FormBaseline.objects.get_or_create(file_type=config["file_type"])
            for field, value in config.items():
                setattr(form_obj, field, value)
            form_obj.save()
            if created:
                self.stdout.write(f"🆕 Created config for {form_obj.file_type}")
            else:
                self.stdout.write(f"✅ Updated config for {form_obj.file_type}")
