FROM python:3.7-buster

WORKDIR /app

COPY ./requirements.txt .

RUN apk add --no-cache --update python3 python3-dev gcc gfortran musl-dev g++ libffi-dev openssl-dev libxml2 libxml2-dev libxslt libxslt-dev libjpeg-turbo-dev zlib-dev

RUN pip install --upgrade cython
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt 

COPY . .

EXPOSE 5000

ENV FLASK_APP=setup.py

CMD ["flask", "run", "-h", "0.0.0.0", "--port", "5000"]
