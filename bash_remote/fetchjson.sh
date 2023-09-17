#!/bin/bash
set -e
ssh honest_snipe << EOF
cd chormeisterweb/Chormeister
docker exec chormeister-web python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent=2 > dumps/dump.json
EOF
source ./.envs/.env
scp $SRVR_USER@honest_snipe:~/chormeisterweb/Chormeister/dumps/dump.json dumps/$(date +"%Y%m%d_%H%M%S").json
