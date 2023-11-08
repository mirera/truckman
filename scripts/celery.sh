#!/usr/bin/bash
sudo cp /home/ubuntu/truckman/celery/celery-beat-truckman.service  /etc/systemd/system/celery-beat-truckman.service
sudo cp /home/ubuntu/truckman/celery/celery-worker-truckman.service  /etc/systemd/system/celery-worker-truckman.service

sudo systemctl daemon-reload
sudo systemctl start celery-beat.service
sudo systemctl enable celery-beat.service 

sudo systemctl start celery-worker.service
sudo systemctl enable celery-worker.service 

