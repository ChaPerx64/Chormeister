#!/bin/bash
source venv/bin/activate
source .DJANGO_SECRET_KEY
gunicorn -c config/gunicorn/dev.py
systemctl start nginx
