from celery import Celery, Task
from app import create_app

flask_app = create_app()

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/1",
    backend="redis://localhost:6379/2",
    include=["tasks"]
)

class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = FlaskTask