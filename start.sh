#!/bin/bash
ps aux | grep gunicorn | grep chormeister | awk '{print $2}' | xargs kill -HUP
source venv/bin/activate
mkdir -pv /var/{log,run}/gunicorn/
gunicorn -c config/gunicorn/dev.py
systemctl restart nginx
