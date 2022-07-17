#!/bin/sh
source venv/bin/activate
export FLASK_APP=setup.py
export FLASK_DEBUG=1
flask run -h 0.0.0.0
