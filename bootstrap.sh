#!/bin/sh
source venv/scripts/activate
export FLASK_APP=setup.py
flask run -h 0.0.0.0
