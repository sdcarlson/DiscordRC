#!/bin/bash

: "${MONGO_USERNAME:?Set MONGO_USERNAME (see .env.example)}"
: "${MONGO_PASSWORD:?Set MONGO_PASSWORD (see .env.example)}"

docker pull mongo # run this command only the first time you set up this container

docker run -d \
  --name mongodb-container \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME="$MONGO_USERNAME" \
  -e MONGO_INITDB_ROOT_PASSWORD="$MONGO_PASSWORD" \
  -e MONGO_INITDB_DATABASE=db \
  mongo
