FROM node:16-alpine@sha256:a1f9d027912b58a7c75be7716c97cfbc6d3099f3a97ed84aa490be9dee20e787 as tsiantuan
WORKDIR /assets
COPY tsiantuan/package.json .
COPY tsiantuan/package-lock.json .
RUN npm ci
COPY tsiantuan/ .
RUN sed 's+https://itaigi.tw/+/+g' -i src/後端.jsx
RUN npm run build

FROM python:3.6-bullseye@sha256:f8652afaf88c25f0d22354d547d892591067aa4026a7fa9a6819df9f300af6fc
MAINTAINER sih4sing5hong5

# Debian bullseye已經EOL，套件搬去archive.debian.org
RUN printf '%s\n' \
  'deb http://archive.debian.org/debian bullseye main' \
  'deb http://archive.debian.org/debian bullseye-updates main' \
  'deb http://archive.debian.org/debian-security bullseye-security main' \
  > /etc/apt/sources.list && \
  rm -f /etc/apt/sources.list.d/*.list
RUN apt-get update && \
  apt-get install -y locales zlib1g-dev libffi-dev libxml2-dev libxslt1-dev rabbitmq-server # 為了編譯, 連google oauth2, message queue

WORKDIR /opt
COPY server-side/requirements.txt .
RUN pip install -r requirements.txt
COPY server-side/ .
ENV DJANGO_SETTINGS_MODULE=itaigi.settings_tsiunnsuann

COPY --from=tsiantuan /assets/build/ whitenoise_static/tsiantuan/

EXPOSE 8000
CMD python manage.py collectstatic --no-input && \
  gunicorn -b 0.0.0.0:8000 \
  --workers 2 --threads 5 \
  --max-requests 1000 \
  --log-level debug \
  itaigi.wsgi
