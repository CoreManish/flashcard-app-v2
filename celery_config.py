from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379',
        broker='redis://localhost:6379'
    )
    

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
