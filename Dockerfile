FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN apk update && apk add --no-cache build-base
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=setup.py

CMD ["flask", "run", "-h", "0.0.0.0", "--port", "5000"]
