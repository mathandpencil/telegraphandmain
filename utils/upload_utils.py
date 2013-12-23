import os
import sys
import json
import uuid
from django.conf import settings
from io import FileIO, BufferedWriter
from django.conf import settings
from django import http
from utils.s3 import upload_to_s3
		
def save_upload( uploaded, filename, raw_data, folder ):

	uid			= str(uuid.uuid4())
	extension	= os.path.splitext(filename)[1]	 
	cloud_name	= uid + extension
		
	try:
		os.mkdir(os.path.join(settings.PROJECT_PATH, folder))
	except:
		pass
	
	local_file_path		= os.path.join( settings.PROJECT_PATH, folder, cloud_name )
	non_absolute_path	= os.path.join( '/', folder, cloud_name  )
		
	with BufferedWriter( FileIO( local_file_path, "w" ) ) as dest:
		if raw_data:
			foo = uploaded.read( 1024 )
			while foo:
				dest.write( foo )
				foo = uploaded.read( 1024 ) 
		else:
			for c in uploaded.chunks():
				dest.write( c )
		
		url = upload_to_s3(file_name=cloud_name, path=local_file_path)
				
		return (True, url)

	return (False, None)