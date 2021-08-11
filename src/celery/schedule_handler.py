from celery.schedules import crontab

from src.bases.celery.generator import Generator

from config import CeleryConfig

generator = Generator(
    name='ScheduleHandler',
    config=CeleryConfig,
)
app = generator.run()

app.conf.beat_schedule = {

}
