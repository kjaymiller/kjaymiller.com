#!/bin/sh
rm -rf output
tailwindcss -c tailwind.config.js -i tailwind.css -o static/css/tailwind.css --minify
render-engine build routes:mysite