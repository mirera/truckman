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

sudo cp /home/ubuntu/truckman/redis/redis.service  /etc/systemd/system/redis.service
sudo cp /home/ubuntu/truckman/celery/celery-beat-truckman.service  /etc/systemd/system/celery-beat-truckman.service
sudo cp /home/ubuntu/truckman/celery/celery-worker-truckman.service  /etc/systemd/system/celery-worker-truckman.service 

# Start Redis on port 
redis-server --port 6379 --daemonize yes --logfile /home/ubuntu/truckman/truckman/redis.log

sudo systemctl daemon-reload

#sudo systemctl start redis.service
#sudo systemctl enable redis.service 

sudo systemctl start celery-beat-truckman
sudo systemctl enable celery-beat-truckman

sudo systemctl start celery-worker-truckman
sudo systemctl enable celery-worker-truckman


#celery -A truckman beat &
#celery -A truckman worker --logfile=/home/ubuntu/truckman/truckman/celery.log --detach

