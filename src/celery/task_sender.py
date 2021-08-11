from src.bases.celery.generator import Generator

from config import CeleryConfig

generator = Generator(
    name='TaskSender',
    config=CeleryConfig,
)

sender = generator.run()
