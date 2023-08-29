FROM python:3.10.10

WORKDIR /code/app

COPY ./requirements.txt /code/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

COPY . /code/app

CMD uvicorn app.app:app --host 0.0.0.0 --port ${PORT:-8080}
