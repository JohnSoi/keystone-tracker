from celery import Celery

from app.core.config import AppSettings, get_app_settings

app_settings: AppSettings = get_app_settings()

celery_app: Celery = Celery("keystone", broker=app_settings.redis_url, backend=app_settings.redis_url)
celery_app.autodiscover_tasks(packages=["app.worker"])
