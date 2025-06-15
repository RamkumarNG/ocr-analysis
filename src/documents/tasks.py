from django.utils import timezone

from celery import shared_task

from .models import Job, OcrResult
from configs.models import FormBaseline
from .helpers import simulate_ocr_results, detect_position_outliers, detect_font_outliers

@shared_task
def analyze_pdf_task(job_id):
    try:
        print("analyze_pdf_task task start......🚀🚀🚀🚀🚀🚀🚀")
        job = Job.objects.select_related('document').get(id=job_id)

        job.started_at = timezone.now()
        job.status = Job.Status.RUNNING
        job.save()

        document_path = job.document.file.path

        form = FormBaseline.objects.get(file_type=job.document.doc_type)

        ocr_raw_data = simulate_ocr_results(
            document_path, allowed_font_style=form.base_font_names, allowed_font_size=form.base_font_size,
            allowed_tolerance = form.font_size_tolerance
        )

        ocr_results = [
            OcrResult(
                job=job,
                page_number=data["page_number"],
                bbox=data["bbox"],
                font=data["font"],
                size=data["size"],
                text=data["text"],
                field_type=data["field_type"],
                meta=data["meta"],
                is_outlier=data["is_outlier"]
            )
            for data in ocr_raw_data
        ]
            
        OcrResult.objects.bulk_create(ocr_results)
        
        ocr_queryset = OcrResult.objects.filter(job=job)
        user_fields = []

        for ocr in ocr_queryset:
            if ocr.field_type == "user":
                user_fields.append({
                    "ocr_result": ocr,
                    "text": ocr.text,
                    "bbox": ocr.bbox,
                    "font": ocr.font,
                    "size": ocr.size,
                    "meta": ocr.meta or []
                })
        
        detect_font_outliers(user_fields, outlier_threshold=0.1)
        detect_position_outliers(user_fields, x_tolerance=15)

        updated_ocr_results = []
        for field in user_fields:
            ocr = field["ocr_result"]
            ocr.meta = field.get("meta", [])
            ocr.is_outlier = field.get("is_outlier", False)
            updated_ocr_results.append(ocr)
        
        OcrResult.objects.bulk_update(updated_ocr_results, ["meta", "is_outlier"])
        
        job.status = Job.Status.COMPLETED
        job.finished_at = timezone.now()
        job.save()

        print("analyze_pdf_task task done......🏝️🏝️🏝️🏝️🏝️🏝️")
        

    except Exception as e:
        print("analyze_pdf_task task failed......")
        job.status = Job.Status.FAILED
        job.error_message = str(e)
        job.finished_at = timezone.now()
        job.save()
        raise

