FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 sentinela
COPY *.py ./
COPY components/ ./components/
COPY dados/bloqueadas.txt ./dados/bloqueadas.txt
RUN chown -R sentinela:sentinela /app
USER sentinela
VOLUME ["/app/dados"]
CMD ["python", "main.py", "--terminal"]
