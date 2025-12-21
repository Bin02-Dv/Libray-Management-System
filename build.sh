#!/bin/bash
# Exit on error
set -o errexit

# Install requirements
pip install -r requirements.txt

# Collect static files
python3.13 manage.py collectstatic --noinput
# Be sure to use the correct python version (e.g. python3.9, python3.10)