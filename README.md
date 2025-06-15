# 📝 OCR Analysis Platform

A Django-based backend for document OCR analysis, outlier detection, and job management. Supports asynchronous processing with Celery and Redis, and stores results in PostgreSQL.

## ✨ Features

- 📄 Upload and manage documents (PDFs)
- ⚙️ Asynchronous OCR analysis jobs using Celery
- 🕵️ Outlier detection for font and position in extracted fields
- 🔗 REST API for documents, jobs, and configuration management
- 🛠️ Configurable baseline font settings per document type
- 🐳 Dockerized for easy deployment

## 🗂️ Project Structure

```
.
├── docker-compose.yml
├── src/
│   ├── app/                # Django project settings and entrypoints
│   ├── documents/          # Document OCR logic, models, tasks, API
│   ├── configs/            # Baseline configuration models and API
│   ├── manage.py
│   ├── requirements.txt
│   └── start.sh
└── README.md
```

## 🚀 Getting Started

### 🛠️ Prerequisites

- Docker & Docker Compose
- or colima installation -> refer: https://formulae.brew.sh/formula/colima

### ⚡ Quick Start

1. **Clone the repository:**

   ```sh
   git clone https://github.com/RamkumarNG/ocr-analysis.git
   cd ocr-analysis
   ```
2. **Build and start the services:**

   ```sh
   colima start or docker-desktop
   docker-compose up --build
   ```
3. **Access the API:**

   - The backend API will be available at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)

## 📡 API Endpoints

- `GET /api/v1/ping` — Health check
- `POST /api/v1/documents/` — Upload a document
  - **Request:** Multipart form data
  - **Fields:**
    - `file`: File to upload
    - `doc_type`: Document type
- `GET /api/v1/documents/` — List documents
- `GET /api/v1/jobs/` — List jobs
- `GET /api/v1/jobs/<job_id>/` — Get job details and OCR results

### Filtering

#### `GET /api/v1/jobs/<job_id>/`

- `field_type`: Filter by field type (`user`, `template`, `other`)
- `is_outlier`: Filter by outlier status (`true`, `false`)
- `operator`: Combine filters using logical operator (`and` (default), `or`)
- `with`: Comma-separated list of extra fields to include in the response (e.g., `with=meta,font`)

**Example:**

```
GET /api/v1/jobs/<job_id>/?field_type=user&is_outlier=true&operator=and
```

#### `GET /api/v1/jobs/`

- `status`: Filter by job status (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`)

**Example:**

```
GET /api/v1/jobs/?status=COMPLETED
```

## ⚙️ Configuration

- Baseline font and size settings are managed via the `configs` app and can be initialized with:
  ```sh
  docker-compose exec backend python manage.py init_form_baseline_configs
  ```

## 👩‍💻 Development

- Code is formatted with [Black](https://black.readthedocs.io/).
- Main dependencies: Django, Django REST Framework, Celery, Redis, PostgreSQL, PyMuPDF.
