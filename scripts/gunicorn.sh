#!/usr/bin/bash
sudo cp /home/ubuntu/truckman/gunicorn/truckman_gunicorn.socket  /etc/systemd/system/truckman_gunicorn.socket
sudo cp /home/ubuntu/truckman/gunicorn/truckman_gunicorn.service  /etc/systemd/system/truckman_gunicorn.service

sudo systemctl start truckman_gunicorn.service
sudo systemctl enable truckman_gunicorn.service  
