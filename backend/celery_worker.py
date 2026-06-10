from celery import Celery, Task
import sys
import os

sys.path.insert(0, '/app')

def make_celery():
    celery_app = Celery(
        "tasks",
        broker=os.getenv("REDIS_URL"), 
        backend=os.getenv("REDIS_URL"),  
        include=["tasks"]
    )
    return celery_app

celery_app = make_celery()

class FlaskTask(Task):
    def __call__(self, *args, **kwargs):
        from app import create_app
        flask_app = create_app()
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = FlaskTask