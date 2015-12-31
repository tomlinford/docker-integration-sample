FROM python:3.5.1

ADD repos/app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 8000
WORKDIR /app
