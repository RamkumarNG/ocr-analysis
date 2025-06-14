from django.db import models

import uuid

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doc_type = models.CharField(max_length=15, null=False, blank=False)
    file = models.FileField(upload_to='uploaded_files/')
    name = models.TextField(null=False)
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table='document'
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['created_at']),
        ]

class Job(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        RUNNING = 'RUNNING', 'Running'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='jobs')
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING,)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'job'
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['created_at']),
            models.Index(fields=['document'])
        ]

class OcrResult(models.Model):

    FIELD_TYPE_CHOICES = [
        ('template', 'Template Field'),
        ('user', 'User Field'),
        ('other', 'Other / Unknown')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page_number = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='ocr_results')
    bbox = models.JSONField(null=True)
    font = models.TextField(null=True, blank=True)
    size = models.FloatField(null=True)
    text = models.TextField(null=True)
    field_type = models.CharField(max_length=10, choices=FIELD_TYPE_CHOICES, default='other')
    order = models.PositiveIntegerField(default=0)
    is_outlier = models.BooleanField(default=False)
    meta = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'ocr_results'
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['job']),
            models.Index(fields=['field_type'])
        ]
