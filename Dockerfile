FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=setup.py

CMD ["flask", "run", "-h", "0.0.0.0", "--port", "5000"]
