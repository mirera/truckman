#!/usr/bin/bash
sudo cp /home/ubuntu/truckman/celerey/celery-beat.service  /etc/systemd/system/celery-beat.service
sudo cp /home/ubuntu/truckman/celerey/celery.service  /etc/systemd/system/celery.service 

sudo systemctl daemon-reload
sudo systemctl start celery-beat.service
sudo systemctl enable celery-beat.service 

sudo systemctl start celery.service
sudo systemctl enable celery.service 