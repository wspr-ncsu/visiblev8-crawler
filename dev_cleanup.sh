#!/bin/bash

docker compose down

(cd screenshots && pwd && sudo rm -rf *)
(cd har && pwd && sudo rm -rf *)

sudo true
sudo rm -rf ./vv8db2
sudo rm -rf ./mongo/data

docker compose up --build --remove-orphans
