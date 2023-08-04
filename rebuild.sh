#!/bin/bash
docker image prune -f
docker compose rm -sv -f
docker compose up --build
