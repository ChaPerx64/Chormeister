#!/bin/bash
source venv/bin/activate
mkdir -pv /var/{log,run}/gunicorn/
gunicorn -c config/gunicorn/dev.py
systemctl restart nginx
