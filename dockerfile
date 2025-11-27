# ---- Base Image ----
FROM python:3.11-slim

# ---- Work Directory ----
WORKDIR /app

# ---- Install system dependencies ----
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy project ----
COPY . /app

# ---- Install Python dependencies ----
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ---- Copy entrypoint ----
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ---- Expose Port ----
EXPOSE 8000

# ---- Start App ----
CMD ["/entrypoint.sh"]
