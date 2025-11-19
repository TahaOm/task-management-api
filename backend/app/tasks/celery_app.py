from celery import Celery

celery = Celery("tasks", broker="redis://redis:6379/1", backend="redis://redis:6379/2")

celery.autodiscover_tasks(["app.tasks"])
