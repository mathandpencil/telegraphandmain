import os
import sys;sys.path.append("../")
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings


def get_signed_url( file_name_on_s3, bucket_name=settings.AWS_BUCKET_NAME):
	conn 		= boto.connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)	
	bucket		= conn.get_bucket(bucket_name)
	key 		= boto.s3.key.Key(bucket)
	key.name 	= file_name_on_s3
	return key.generate_url(expires_in=1000, force_http=True)

def save_file_in_s3(filename):
	conn   = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
	bucket = conn.get_bucket(settings.AWS_BUCKET_NAME)
	k	   = Key(bucket)
	k.key  = filename
	k.set_contents_from_filename(filename)

def upload_to_s3(file_name, path, force_download=False):
	#connection = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)	
	connection 		= boto.connect_s3(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)	
	bucket = connection.lookup( settings.AWS_BUCKET_NAME )
	
	key = boto.s3.key.Key(bucket)
	key.name = file_name
	key.set_contents_from_filename(path)
	key.make_public()

	return key.generate_url(expires_in=0, query_auth=False)
	

def delete_from_s3(image_name):
	connection = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)	
	bucket = connection.lookup(settings.AWS_BUCKET_NAME)
	key = bucket.lookup(image_name)
	if key is None:
		return False
	else:
		key.delete()
		return True
