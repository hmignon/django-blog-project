FROM python:3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HEROKU_APP_NAME $HEROKU_APP_NAME
ENV PORT 8080

COPY . .

RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps && \
  python3 manage.py collectstatic --noinput --clear && \
  python3 manage.py dumpdata -o data.json

CMD python manage.py runserver 0.0.0.0:$PORT