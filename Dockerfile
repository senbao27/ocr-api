FROM python:3.10-slim
RUN apt-get update && apt-get install -y libglib2.0-0 libgl1 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch torchvision
ENV PYTHONUNBUFFERED=1
RUN python - <<'PY'
import easyocr
easyocr.Reader(['en','ch_sim'])
PY
COPY . .
EXPOSE 8000
CMD ["gunicorn","--workers","2","--threads","4","--bind","0.0.0.0:8000","app:app"]
