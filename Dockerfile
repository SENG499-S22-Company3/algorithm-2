FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN apk --update add gcc build-base freetype-dev libpng-dev openblas-dev
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt --no-cache-dir 

COPY . .

EXPOSE 5000

ENV FLASK_APP=setup.py

CMD ["flask", "run", "-h", "0.0.0.0", "--port", "5000"]
