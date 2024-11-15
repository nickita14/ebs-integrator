FROM python:3.13-slim as build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        pkg-config \
        libmariadb-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --upgrade pip

RUN pip3 install --no-cache-dir --no-warn-script-location \
        uwsgi \
        Django \
        djangorestframework \
        requests \
        psycopg2-binary \
        celery>=5.3.1 \
        redis>=4.6.0 \
        django-cors-headers \
        django-redis \
        drf-spectacular \
        drf-standardized-errors[openapi]

FROM python:3.13-slim as runtime

WORKDIR /var/www/backend

COPY --from=build /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

COPY . /var/www/backend

EXPOSE 5000
EXPOSE 5678

RUN pip3 install --no-cache-dir --no-warn-script-location \
        debugpy

CMD ["sh", "-c", "python3 -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:5000"]
