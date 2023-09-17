#!/bin/bash
docker image prune -f
docker compose rm -sv -f
docker volume rm chormeister-db-volume
docker volume rm chormeister-static-volume
docker volume rm chormeister-media-volume
while getopts "d" option; do
    case $option in
        d) 
            docker compose up --build -d
            exit;;
    esac
done
docker compose up --build
