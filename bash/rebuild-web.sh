#!/bin/bash
docker stop chormeister-web
docker rm chormeister-web
docker image rm chormeister-web
while getopts "d" option; do
    case $option in
        d) 
            docker compose up --no-deps --force-recreate --build web -d
            exit;;
    esac
done
docker compose up --no-deps --force-recreate --build web --attach-dependencies web server db
