#!/bin/bash
docker image prune -f
docker compose rm -sv -f
docker volume rm chormeister_postgres_data
docker compose up --build
