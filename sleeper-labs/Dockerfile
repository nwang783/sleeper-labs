FROM python:3.13-slim
RUN pip install --no-cache-dir fastapi==0.135.1 httpx==0.28.1
WORKDIR /app
COPY ownership_worker.py /app/ownership_worker.py
USER 65534:65534
ENTRYPOINT ["python", "/app/ownership_worker.py", "--worker"]
