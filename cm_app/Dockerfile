FROM python:3.11.4-alpine3.18

WORKDIR /usr/src/cm_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/cm_app/entrypoint.sh
RUN chmod +x /usr/src/cm_app/entrypoint.sh

COPY . .

ENTRYPOINT ["sh", "/usr/src/cm_app/entrypoint.sh"]
