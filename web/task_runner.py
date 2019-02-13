from web import create_app
import sys
from rq import get_current_job
from web import db
from web.models import Task
from web import mail_helper

app = create_app()
app.app_context().push()

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()

        if progress >= 100:
            task = Task.query.get(job.get_id())
            task.complete = True
            db.session.commit()

def send_email(to, subject, content):
    try:
        mail_helper.send_html_email(to, subject, content)
        _set_task_progress(100)
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())