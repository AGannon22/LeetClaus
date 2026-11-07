FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app \
    WEB_CONCURRENCY=3

COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

COPY . .

# Don't run the app as root.
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

# Production server. WEB_CONCURRENCY sets the number of workers; PORT is honored
# for hosts (Render, Railway, ...) that assign one. Dev overrides this command
# in docker-compose.override.yml.
CMD exec gunicorn --bind 0.0.0.0:${PORT:-5000} --access-logfile - app:app
