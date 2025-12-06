FROM python:3.11-slim

RUN useradd -m appuser

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app /app

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 9000

ENV APP_ENV=container

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
