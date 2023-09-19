#!/usr/bin/bash
sudo cp /home/ubuntu/truckman/redis/redis.service  /etc/systemd/system/redis.service

sudo systemctl daemon-reload
sudo systemctl start redis.service
sudo systemctl enable redis.service 