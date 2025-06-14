from django.db import models

class FormBaseline(models.Model):
    file_type = models.CharField(max_length=20, primary_key=True)
    base_font_names = models.JSONField(default=list)
    base_font_size = models.JSONField(default=list)
    font_size_tolerance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.file_type} baseline"
