# TrainTrack Dockerfile

FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App files (overridden by bind mounts in dev/prod)
COPY . .

# Wait script
COPY wait-for-mariadb.sh /wait-for-mariadb.sh
RUN chmod +x /wait-for-mariadb.sh

EXPOSE 5000

CMD ["/wait-for-mariadb.sh", "gunicorn", "--workers=2", "--threads=4", \
     "--worker-class=gthread", "--bind=0.0.0.0:5000", \
     "--timeout=120", "--access-logfile=-", "app:app"]
