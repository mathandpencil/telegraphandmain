from __future__ import with_statement
import os, sys, time, getpass
from fabric.api import *
from fabric.colors import red, green, blue, cyan, magenta, white, yellow
from fabric.api import put, run, settings, sudo
from fabric.operations import prompt
from fabric.contrib import django

env.REMOTE_CODEBASE_PATH		= '/home/ubuntu/mathandpencil'
env.VENDOR_PATH					= "/home/ubuntu/code"
env.BUILD_FOLDER				= "/home/ubuntu/build"
env.PIP_REQUIREMENTS_PATH		= 'config/requirements.txt'
env.GUNICORN_PID_PATH			= os.path.join(env.REMOTE_CODEBASE_PATH, 'logs/gunicorn.pid')
env.PROJECT_PATH				= os.path.dirname(os.path.abspath(__file__))
env.MATHANDPENCIL_PATH				= "/home/ubuntu/mathandpencil/"
env.BRANCH_NAME					= 'master'
env.user						= 'ubuntu'

import platform
if platform.system() == "Windows":
	env.key_filename = 'C:\\Users\\%s\\.ssh\\id_rsa' % getpass.getuser()
	IS_WINDOWS = True
else:
	env.key_filename = '/Users/%s/.ssh/id_rsa' % getpass.getuser()
	IS_WINDOWS = False

env.roledefs = {
}

def bootstrap():
	with cd(env.MATHANDPENCIL_PATH):
		run("./manage.py bootstrap")

def upgrade_ubuntu():
	sudo('do-release-upgrade')

def setup_apt_get(upgrade=False):
	""" Install all apt-get packages """
	if upgrade:
		sudo('apt-get -y update')
		sudo('apt-get -y upgrade')
	
	sudo('apt-get -y install python-pip ')

def setup_install():
	packages = [
		'build-essential',
		'gcc',
		'iotop',
		'git',
		'python-dev',
		'make',
	]
	sudo('apt-get -y update')
	sudo('DEBIAN_FRONTEND=noninteractive apt-get -y --force-yes upgrade')
	sudo('DEBIAN_FRONTEND=noninteractive apt-get -y --force-yes install %s' % ' '.join(packages))
	
def tail():
	run('tail -n 150 /var/logs/celery_gunicorn.log')
	
def pip_install():
	""" Install requirements.txt using python pip """
	with cd(env.MATHANDPENCIL_PATH):
		#sudo('chown -R ubuntu.ubuntu /home/ubuntu/.pip/')
		sudo('pip install -r %s' % env.PIP_REQUIREMENTS_PATH)
		
def deploy():
	""" Install requirements.txt using python pip """
	with cd(env.MATHANDPENCIL_PATH):
		run('git pull')
		run('cp mathandpencil/local_settings.production mathandpencil/local_settings.py')
	compress_assets()
	transfer_assets()	
	cleanup_assets()
	sudo('supervisorctl reload')
	
	
def make_directories():
	sudo('touch /var/log/mathandpencil.log')
	sudo('chmod -R 777 /var/log/mathandpencil.log')
	sudo('mkdir -p /var/logs/gunicorn/')
	sudo('chmod -R 777 /var/logs/gunicorn/')
	
def setup_supervisor():
	with cd(env.MATHANDPENCIL_PATH):
		put('config/supervisor_gunicorn.conf', '/etc/supervisor/conf.d/mathandpencil.conf', use_sudo=True)
		sudo('supervisorctl update')
		sudo('supervisorctl reload')
	
def build_all():
	setup_apt_get()
	setup_pip_requirements()
	

def configure_nginx():
	with cd(env.MATHANDPENCIL_PATH):
		put("config/nginx.mathandpencil.conf", "/usr/local/nginx/conf/sites-enabled/mathandpencil.conf", use_sudo=True)
	sudo('service nginx restart')
	
	
def compress_assets(bundle=False):
	"""
		Use jammit to compress assets
	"""
	local('jammit -c assets.yml --base-url https://www.socialq.com --output static')
	local('tar -czf static.tgz static/*')

def transfer_assets():
	"""
		Transfer compressed assets to EC2
	"""
	run('mkdir -p %s/static/' % env.MATHANDPENCIL_PATH)
	put('static.tgz', '%s/static/' % env.MATHANDPENCIL_PATH)
	with cd(env.MATHANDPENCIL_PATH):
		run('tar -xzf static/static.tgz')
		run('rm -f static/static.tgz')

def cleanup_assets():
	"""
		Delete compress (static.tgz) files locally.
	"""
	local('rm -f static.tgz')
	