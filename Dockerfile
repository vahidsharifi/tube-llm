FROM python:3.11

WORKDIR /code/app

COPY ./requirements.txt /code/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

COPY . /code/app

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
#
# Use the official Python image from Docker Hub
#FROM python:3.9-slim
#
## Set the working directory
#WORKDIR /app
#
## Copy the requirements file
#COPY requirements.txt .
#
## Install dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#
## Copy the rest of the application code
#COPY . .
#
## Expose the port the app runs on
#EXPOSE 8080
#
## Command to run the application
#CMD ["python", "app.py"]
