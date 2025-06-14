from rest_framework import serializers

from .models import FormBaseline

class FormBaseLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormBaseline
        fields = [
            'file_type', 'base_font_names',
            'base_font_size', 'font_size_tolerance'
        ]