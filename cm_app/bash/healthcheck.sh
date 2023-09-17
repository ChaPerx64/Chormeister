#!/bin/sh
RESP=$(curl -LI http://localhost:8000/ -o /dev/null -w '%{http_code}' -s)
if [ $RESP != 200 ]; then
    exit 1
fi
