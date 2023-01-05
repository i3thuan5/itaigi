FROM node:16-alpine as tsiantuan
WORKDIR /assets
COPY tsiantuan/package.json .
COPY tsiantuan/package-lock.json .
RUN npm ci
COPY tsiantuan/ .
RUN npm run build

FROM python:3.6-buster
MAINTAINER sih4sing5hong5

RUN apt-get update && \
  apt-get install -y locales zlib1g-dev libffi-dev libxml2-dev libxslt1-dev rabbitmq-server # 為了編譯, 連google oauth2, message queue

WORKDIR /opt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --no-input
COPY --from=tsiantuan /assets/build/ whitenoise_static

EXPOSE 8000
CMD gunicorn -b 0.0.0.0:8000 \
  --workers 2 --threads 5 \
  --max-requests 1000 \
  --log-level debug \
  itaigi.wsgi
