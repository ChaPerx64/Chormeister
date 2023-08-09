#!/bin/bash
docker image prune -f
docker compose rm -sv -f
while getopts "d" option; do
    case $option in
        d) 
            docker compose up --build -d
            exit;;
    esac
done
docker compose up --build
