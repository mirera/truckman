#!/usr/bin/bash 

# Activate the virtual environment
source /home/ubuntu/truckman_env/bin/activate

# stop running services, if any
#redis-cli shutdown

sed -i 's/\[]/\["truckman.loginit.co.ke"]/' /home/ubuntu/truckman/truckman/settings.py 
sudo cp /home/ubuntu/truckman_secrets/.env  /home/ubuntu/truckman/.env 
cd /home/ubuntu/truckman && python manage.py makemigrations
cd /home/ubuntu/truckman && python manage.py migrate      
cd /home/ubuntu/truckman && python manage.py collectstatic
sudo service gunicorn restart
sudo service nginx restart


# Start Redis on port 
redis-server --port 6379 --daemonize yes --logfile /home/ubuntu/truckman/truckman/redis.log
cd /home/ubuntu/truckman && celery -A truckman beat &
cd /home/ubuntu/truckman && celery -A truckman worker --logfile=/home/ubuntu/truckman/truckman/celery.log --detach

