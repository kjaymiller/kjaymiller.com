#!/bin/sh
rm -rf output
tailwindcss -c tailwind.config.js -i tailwind.css -o static/css/tailwind.css --minify
python routes.py