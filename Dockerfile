FROM python:3.10-buster

WORKDIR /app

COPY ./requirements.txt .

# RUN apk add --no-cache --update python3 python3-dev gcc gfortran musl-dev g++ libffi-dev openssl-dev libxml2 libxml2-dev libxslt libxslt-dev libjpeg-turbo-dev zlib-dev

RUN pip install --upgrade cython
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt 

COPY . .

ENV PORT=5000
EXPOSE 5000

ENV FLASK_APP=setup.py

RUN python3.10 -m venv venv

CMD ["/app/bootstrap.sh"]
