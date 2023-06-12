#!/bin/bash
source venv/bin/activate
source .DJANGO_SECRET_KEY
mkdir -pv /var/{log,run}/gunicorn/
gunicorn -c config/gunicorn/dev.py
systemctl start nginx
