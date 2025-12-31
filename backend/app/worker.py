"""Celery worker configuration for background job processing."""

from celery import Celery

import app.models  # noqa: F401 - Register models
from app.core.config import settings

# Initialize Celery app
celery_app = Celery(
    "cmatrix",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    result_extended=True,  # Store extended task result metadata
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    task_soft_time_limit=3300,  # 55 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
    result_expires=604800,  # Results expire after 7 days
)

# Auto-discover tasks from all registered apps
celery_app.autodiscover_tasks(["app.tasks"])

if __name__ == "__main__":
    celery_app.start()
