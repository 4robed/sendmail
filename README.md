# SENDMAIL service

## Requirements
- Ubuntu 18.04
- Python 3.6+

## Configuration
create env.yaml in project directory

```.yaml
ENVIRONMENT: 'local'

SECRET_KEY: ''

SENTRY_DNS: ''

REDIS:
  password: ''
  host: 'localhost'
  port: 6379

LOG_FILE: 'tmp/output.log'
```

## Setup
`pip3 install pipenv`

`pipenv install`

## Run
sample: `pipenv run python run.py api`

##### Celery worker
`pipenv python run.py celery`

## DOC
TODO


# docker
- kill all container: `docker system prune`
- kill all images: `docker rmi -f $(docker images -a -q)`
- delete image:  `docker rmi <name>:<tag>`
- build: `docker build -t sendmail .`
- run: `docker run -dp 5000:5000 sendmail`