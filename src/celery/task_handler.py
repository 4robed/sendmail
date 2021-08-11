from src.bases.celery.generator import Generator
from src.databases import Redis

from config import REDIS, CeleryConfig

from . import tasks

redis = Redis(**REDIS, db=1)


generator = Generator(
    name='TaskHandler',
    redis=redis,
    config=CeleryConfig,
    task_module=tasks,
    task_queues=(
        'SendMail',
    )
)

app = generator.run()
