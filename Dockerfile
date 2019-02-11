# Use an official Python runtime as a parent image
FROM python:3.6-alpine

RUN adduser -D tickerinfo

# Set the working directory to /app
# WORKDIR /home/tickerinfo
WORKDIR /app

# Copy the current directory contents into the container at /app

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY web web
COPY migrations migrations
COPY app.py config.py boot.sh ./
RUN chmod +x boot.sh

#RUN chown -R tickerinfo:tickerinfo ./
#USER tickerinfo

ENV FLASK_APP app.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
