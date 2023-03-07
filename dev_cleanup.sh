#!/bin/bash

docker compose down

(cd screenshots && rm -rf *)
(cd har && rm -rf *)

sudo true
sudo rm -rf ./vv8db2
sudo rm -rf ./mongo/data

docker compose up --build --remove-orphans
