FROM ubuntu:16.04

MAINTAINER Clément Tailleur "clement.tailleur@gmail"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000
ENTRYPOINT ["python3"]

CMD [ "app.py" ]
