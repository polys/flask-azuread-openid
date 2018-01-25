FROM python:3.6.4-slim

WORKDIR /usr/src/app

# copy requirements.txt and restore packages
COPY requirements.txt ./
RUN pip install -r requirements.txt

# copy everything else
COPY server.py ./

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP server.py

EXPOSE 80

CMD [ "flask", "run", "--host=0.0.0.0", "--port=80" ]