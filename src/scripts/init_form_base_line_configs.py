import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from configs.models import FormBaseline
from django.db import transaction

config_data = [
    {
        "file_type": "itr",
        "base_font_names": ["Times-Bold", "Times-Roman"],
        "base_font_size": [8.0],
    }
]

@transaction.atomic
def main():
    for _config in config_data:
        try:
            form_obj = FormBaseline.objects.get(
                file_type = _config['file_type'],
            )
        except FormBaseline.DoesNotExist:
            form_obj = FormBaseline()
        
        for option, value in _config.items():
            setattr(form_obj, option, value)

        form_obj.save()


if __name__ == "__main__":
    main()
