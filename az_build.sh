#!/bin/sh
rm -rf output
python -m venv venv
. ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
tailwindcss -c tailwind.config.js -i tailwind.css -o static/css/tailwind.css --minify
python routes.py