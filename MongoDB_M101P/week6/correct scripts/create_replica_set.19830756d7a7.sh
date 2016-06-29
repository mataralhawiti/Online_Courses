#!/usr/bin/env bash

#mkdir -p /data/rs1 /data/rs2 /data/rs3
mongod --replSet m101 --logpath "1.log" --dbpath /home/matar/data/rs1 --port 27017 --oplogSize 64 --fork
mongod --replSet m101 --logpath "2.log" --dbpath /home/matar/data/rs2 --port 27018 --oplogSize 64 --fork
mongod --replSet m101 --logpath "3.log" --dbpath /home/matar/data/rs3 --port 27019 --oplogSize 64 --fork
