FROM python:3.10 AS development

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/requirements-dev.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir djangorestframework django-rest-swagger drf-yasg
COPY linkapp /app