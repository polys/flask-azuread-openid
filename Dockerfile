FROM python:3.6-slim

WORKDIR /usr/src/app

# copy requirements.txt and restore packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy everything else
COPY server.py ./

ENV PYTHONUNBUFFERED 1

EXPOSE 80

CMD [ "gunicorn", "server:app", "-b=0.0.0.0:80" ]