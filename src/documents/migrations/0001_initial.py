# Generated by Django 3.2.25 on 2025-06-14 12:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('doc_type', models.CharField(max_length=15)),
                ('file', models.FileField(upload_to='uploaded_files/')),
                ('name', models.TextField()),
                ('created_at', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'document',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('RUNNING', 'Running'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('result', models.TextField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='documents.document')),
            ],
            options={
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='OcrResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('page_number', models.IntegerField()),
                ('bbox', models.JSONField(null=True)),
                ('font', models.TextField(blank=True, null=True)),
                ('size', models.FloatField(null=True)),
                ('text', models.TextField(null=True)),
                ('field_type', models.CharField(choices=[('template', 'Template Field'), ('user', 'User Field'), ('other', 'Other / Unknown')], default='other', max_length=10)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_outlier', models.BooleanField(default=False)),
                ('meta', models.JSONField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ocr_results', to='documents.job')),
            ],
            options={
                'db_table': 'ocr_results',
            },
        ),
        migrations.AddIndex(
            model_name='document',
            index=models.Index(fields=['id'], name='document_id_1d6415_idx'),
        ),
        migrations.AddIndex(
            model_name='document',
            index=models.Index(fields=['created_at'], name='document_created_71db36_idx'),
        ),
        migrations.AddIndex(
            model_name='ocrresult',
            index=models.Index(fields=['id'], name='ocr_results_id_621d96_idx'),
        ),
        migrations.AddIndex(
            model_name='ocrresult',
            index=models.Index(fields=['job'], name='ocr_results_job_id_a20b9c_idx'),
        ),
        migrations.AddIndex(
            model_name='ocrresult',
            index=models.Index(fields=['field_type'], name='ocr_results_field_t_d6d3b8_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['id'], name='job_id_ba9c34_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['created_at'], name='job_created_010237_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['document'], name='job_documen_4fe326_idx'),
        ),
    ]
