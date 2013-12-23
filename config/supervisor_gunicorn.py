[program:telegraphandmain]
command=gunicorn telegraphandmain.wsgi:application --bind 127.0.0.1:8001
directory=/home/ubuntu/telegraphandmain/
user=ubuntu
stdout_logfile=/var/logs/telegraphandmain_celery_gunicorn.log
stderr_logfile=/var/logs/telegraphandmain_celery_gunicorn.log
autostart=true
autorestart=true
#redirect_stderr=True
priority=991
stopsignal=HUP