FROM python:3.9.4

ARG DJANGO_SETTINGS_MODULE="Backend.settings"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

# Copy project files
COPY . /django
WORKDIR /django

# Update packages, install requirements, and collect static files
RUN apt-get update && \
    pip install pip==22.3.1 && \ 
    pip install -r requirements.txt && \ 
    python src/manage.py collectstatic --noinput
