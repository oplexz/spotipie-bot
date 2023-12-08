FROM python:3.11

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt

# COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt;

ADD . /app

ENTRYPOINT python .
