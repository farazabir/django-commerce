FROM alpine:3.18

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt /backend/requirements.txt

RUN pip install -r requirements.txt

COPY .  /backend

CMD [ "python","manage.py","runserver","0.0.0.0:8000" ]