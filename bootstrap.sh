#!/bin/sh
source venv/bin/activate
export FLASK_APP=./app/index.py
flask run -h 0.0.0.0
