#!/bin/bash

docker pull mongo # run this command only the first time you set up this container

docker run -d \
  --name mongodb-container \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=2BLfv2tcQnSa \
  -e MONGO_INITDB_DATABASE=db \
  mongo
