FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies: build tools for psycopg2 + GEOS for shapely.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libgeos-c1v5 \
    && rm -rf /var/lib/apt/lists/*

# Copy the project and install it (package discovery pinned in pyproject).
COPY . .
RUN pip install --no-cache-dir -e ".[dev]"

# Media directory for the local (non-Azure) storage backend.
RUN mkdir -p /app/media_store
ENV LOCAL_MEDIA_ROOT=/app/media_store

RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
