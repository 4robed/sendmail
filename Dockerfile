FROM python:3.8
MAINTAINER 4robed <n.hung19920@gmail.com>

EXPOSE 5000
RUN mkdir -p /app
WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY . /app

CMD ["pipenv", "run", "python", "run.py", "api", "--host=0.0.0.0", "--port=5000"]