#!/bin/bash

#down docker-composer images
docker-compose down; 

#remove DATABASE FILES
sudo chmod a+r -R /home/xkwna06/Documents/Code/kmanga/pgdata
sudo rm -rf /home/xkwna06/Documents/Code/kmanga/pgdata
sudo ls -la /home/xkwna06/Documents/Code/kmanga/pgdata/*
docker volume prune -f
mkdir ../pgdata

