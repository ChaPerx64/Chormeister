#!/bin/bash
docker image prune -f
docker compose rm -sv -f
docker volume rm chormeister_postgres_data
docker volume rm chormeister_static_volume
while getopts "d" option; do
    case $option in
        d) 
            docker compose up --build -d
            exit;;
    esac
done
docker compose up --build
