#!/bin/bash

sudo -v

git pull

if [ $# -eq 0 ]
  then
    ./install.sh yes
    exit
fi

hash=$(git rev-parse HEAD)

container_name=network-api-$hash

echo "building $container_name"

sudo docker build -t $container_name .

sudo docker stop network-api || true

sudo docker logs network-api >> ./network-api.log 2>&1 || true

echo "Logs for $container_name starting below" >> ./network-api.log

sudo docker rm network-api || true

sudo docker run --restart always -dp 8000:8000 --name network-api $container_name

sudo docker system prune -f
sudo docker image prune -af