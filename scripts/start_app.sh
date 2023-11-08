#!/usr/bin/bash 

# Activate the virtual environment
source /home/ubuntu/truckman_env/bin/activate


sed -i 's/\[]/\["truckman.loginit.co.ke"]/' /home/ubuntu/truckman/truckman/settings.py 
sudo cp /home/ubuntu/truckman_secrets/.env  /home/ubuntu/truckman/.env 
cd /home/ubuntu/truckman && python manage.py makemigrations
python manage.py migrate      
python manage.py collectstatic
sudo service gunicorn restart
sudo service nginx restart

sudo systemctl disable celery-beat-mdeni.service
sudo systemctl stop celery-beat-mdeni.service

sudo systemctl disable celery-worker-mdeni.service
sudo systemctl stop celery-worker-mdeni.service

sudo rm -r /etc/systemd/system/celery-beat-mdeni.service
rm -r /etc/systemd/system/celery-worker-mdeni.service

sudo cp /home/ubuntu/truckman/celery/celery-beat-truckman.service  /etc/systemd/system/celery-beat-truckman.service
sudo cp /home/ubuntu/truckman/celery/celery-worker-truckman.service  /etc/systemd/system/celery-worker-truckman.service 

sudo systemctl daemon-reload
sudo systemctl start celery-beat-truckman
sudo systemctl enable celery-beat-truckman

sudo systemctl start celery-worker-truckman
sudo systemctl enable celery-worker-truckman

# Start Redis on port 
#redis-server --port 6379 --daemonize yes --logfile /home/ubuntu/truckman/truckman/redis.log
#celery -A truckman beat &
#celery -A truckman worker --logfile=/home/ubuntu/truckman/truckman/celery.log --detach

