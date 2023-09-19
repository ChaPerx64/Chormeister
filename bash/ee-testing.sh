#!/bin/sh
docker image prune -f
docker compose down
docker compose -f docker-compose.test.yml rm -svf
docker volume rm test-chormeister-db-volume
docker volume rm test-chormeister-static-volume
docker volume rm test-chormeister-media-volume
docker compose -f docker-compose.test.yml up --build -d
docker build -t chormeister-tester:latest ee-testing
docker run --attach STDOUT --network chormeister_testing --name chormeister-tester chormeister-tester:latest
docker rm chormeister-tester
