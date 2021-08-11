from src.databases import Redis
from src.bases.api.factory import Factory
from src.api import resources

from config import (ApiConfig,
                    REDIS)


redis = Redis(**REDIS, db=1)

factory = Factory(
    config=ApiConfig,
    resource_module=resources,
    redis=redis,
)

app = factory.create_app()
