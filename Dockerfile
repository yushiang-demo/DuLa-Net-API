FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip

#RUN pip install Celery redis Flask Flask-RESTx pymongo pillow
RUN pip install --no-cache-dir -r requirements.txt