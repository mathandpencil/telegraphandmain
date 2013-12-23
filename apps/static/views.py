from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext,Context,Template
from django.core.mail import send_mail,mail_managers
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.core import mail

def index(request):
	return render_to_response('index.html',{})

