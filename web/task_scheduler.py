from web import db
from web.models import User, Task
from flask import current_app

def launch_task(user, name, description, *args, **kwargs):
    rq_job = current_app.task_queue.enqueue('web.task_runner.' + name,
                                            *args, **kwargs)
    task = Task(id=rq_job.get_id(), name=name, description=description,
                user=user)
    db.session.add(task)
    return task

def get_tasks_in_progress(user):
    return Task.query.filter_by(user=user, complete=False).all()

def get_task_in_progress(user, name):
    return Task.query.filter_by(name=name, user=user,
                                complete=False).first()