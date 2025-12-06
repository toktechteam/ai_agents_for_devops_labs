FROM python:3.11-slim

RUN useradd -m appuser
WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app
USER appuser

CMD ["python", "batch_job.py"]
