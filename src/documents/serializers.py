from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from collections import defaultdict

from .models import Document, Job, OcrResult
from .tasks import analyze_pdf_task


class OcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcrResult
        fields = [
            'id', 'bbox', 'font', 'size',
            'text', 'field_type', 'page_number',
            'meta', 'is_outlier'
        ]

class GroupOcrSerializer(serializers.Serializer):
    def to_representation(self, data):
        serialized = OcrSerializer(instance=data, many=True, context=self.context).data
        grouped = defaultdict(list)

        for item in serialized:
            page = str(item['page_number'])
            item.pop('page_number', None)
            grouped[page].append(item)
        
        return grouped

class JobSerializer(serializers.ModelSerializer):
    document_id = serializers.UUIDField(source='document.id', read_only=True)
    job_status = serializers.CharField(source='get_status_display', read_only=True)
    ocr_results = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(JobSerializer, self).__init__(*args, **kwargs)
    
    def get_ocr_results(self, obj):
        request = self.context.get('request')
        query_params = request.query_params
        field_type = query_params.get('field_type')
        is_outlier = query_params.get('is_outlier')
        operator = query_params.get('operator', 'and').lower()

        filters = []
        if field_type:
            filters.append(Q(field_type=field_type))
        
        if is_outlier is not None:
            is_outlier_bool = is_outlier.lower() == "true"
            filters.append(Q(is_outlier=bool(is_outlier_bool)))
        
        if len(filters) > 0:
            query = Q()
            if operator == 'and':
                query = Q()
                for f in filters:
                    query &= f
            elif operator == 'or':
                query = Q()
                for f in filters:
                    query |= f
            else:
                query = Q()

            results_qs = obj.ocr_results.filter(query)
        else:
            results_qs = obj.ocr_results.all()

        
        return GroupOcrSerializer(results_qs).data

    
    class Meta:
        model = Job
        fields = [
            'id', 'document_id', 'job_status',
            'created_at', 'started_at', 'finished_at',
            'result', 'error_message', 'ocr_results'
        ]
        read_only_fields = [
            'id', 'created_at', 'started_at',
            'finished_at', 'result', 'error_message',
        ]


class DocumentSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'name', 'doc_type',
            'file', 'file_url',
            'created_at', 'jobs',
        ]
        read_only_fields = ['id', 'created_at', 'jobs']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'name', 'doc_type']
        read_only_fields = ['id', 'name']

    def create(self, validated_data):
        
        doc_type = validated_data.get('doc_type')
        if not doc_type:
            raise ValidationError("doc_type is required and cannot be empty.")
        
        file = validated_data['file']
        name = file.name.rsplit('.', 1)[0]
        
        document = Document.objects.create(file=file, name=name, doc_type=doc_type)

        job = Job.objects.create(
            document=document,
        )

        analyze_pdf_task.delay(job.id)

        return document
    
