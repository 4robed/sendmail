import inspect
from kombu import Queue
from celery import Celery as _Celery
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from .task import Task


class Celery(_Celery):
    def __init__(self,
                 sql_session_factory=None,
                 redis=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sql_session_factory = sql_session_factory
        self.redis = redis


class Generator(object):
    def __init__(self,
                 name,
                 config,
                 redis=None,
                 task_module=None,
                 task_queues=None):

        self.name = name
        self.config = config
        self.redis = redis
        self.task_module = task_module
        self.task_queues = task_queues

    def _register_tasks(self, worker):
        classes = inspect.getmembers(self.task_module,
                                     inspect.isclass)
        for cls_name, cls in classes:
            if not issubclass(cls, Task):
                continue

            worker.register_task(cls())

    def _declare_queues(self, worker):
        queues = list()
        for queue_name in self.task_queues:
            queues.append(Queue(
                queue_name,
            ))
        worker.conf.task_queues = queues

    def run(self) -> Celery:
        worker = Celery(main=self.name,
                        redis=self.redis)

        worker.config_from_object(self.config)

        if self.task_module:
            self._register_tasks(worker)

        if self.task_queues:
            self._declare_queues(worker)

        if hasattr(self.config, 'sentry_dns'):
            sentry_sdk.init(
                dsn=self.config.sentry_dns,
                environment=self.config.env,
                integrations=[CeleryIntegration()]
            )

        return worker
