FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    libopenjp2-7 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pymupdf==1.26.0 --only-binary pymupdf

# Install OS dependencies required to build PyMuPDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    libopenjp2-7-dev \
    libfreetype6-dev \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Upgrade pip tools
# RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python deps
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY . .

RUN mkdir -p media staticfiles data
RUN chmod -R 777 data media staticfiles
RUN python manage.py collectstatic --noinput

COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
