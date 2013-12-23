import os

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

bind = "127.0.0.1:8001"
pidfile = "/var/logs/gunicorn/telegraphandmain_gunicorn.pid"
logfile = "/var/logs/gunicorn/telegraphandmain_production.log"
accesslog = "/var/logs/gunicorn/telegraphandmain_production.log"
errorlog = "/var/logs/gunicorn/telegraphandmain_errors.log"
loglevel = "debug"
name = "telegraphandmain"
timeout = 60*60	
max_requests = 1000
workers = numCPUs()*3
