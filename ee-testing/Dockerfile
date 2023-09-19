FROM python:3.11.4-alpine3.18

RUN apk add chromium

WORKDIR /usr/src/testing

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN source pathconfig

CMD [ "pytest", "-rP" ]
