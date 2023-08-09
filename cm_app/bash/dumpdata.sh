#!/bin/sh
cd "$(dirname "$0")"
cd ..
# echo $(date +"%Y%m%d_%H%M%S")
python manage.py dumpdata --exclude auth.permission --exclude contenttypes
