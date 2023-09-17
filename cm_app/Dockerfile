FROM python:3.11.4-alpine3.18

RUN apk --update --no-cache add curl

WORKDIR /usr/src/cm_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./bash/entrypoint.sh ./bash/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/cm_app/bash/entrypoint.sh
RUN chmod +x /usr/src/cm_app/bash/entrypoint.sh

COPY . .

RUN mkdir -pv /var/log/gunicorn/
RUN mkdir -pv /var/run/gunicorn/
RUN mkdir -p ./dumps

ENTRYPOINT ["sh", "/usr/src/cm_app/bash/entrypoint.sh"]
