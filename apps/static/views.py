from django import http
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives	
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import authenticate
from mongoengine.django.auth import User
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.core.urlresolvers import reverse

def index(request):
	return render(request, 'static/index.html', {})
	
def about(request):
	return render(request, 'static/about.html', {})
	
def login(request):
	
	if request.method == "POST":
		
		username = request.REQUEST.get("username").strip()
		password = request.REQUEST.get("password").strip()
		user = authenticate( username=username, password=password )
		if user:
			auth_login(request, user)
			return http.HttpResponseRedirect(reverse('blog-new-post'))
		else:
			pass
			
	return render(request, 'static/login.html', {})
	
def branding_1(request):
	return render(request, 'static/branding_1.html', {})
	
def branding_2(request):
	return render(request, 'static/branding_2.html', {})
	
def branding_3(request):
	return render(request, 'static/branding_3.html', {})
	
def capabilities(request):
	return render(request, 'static/capabilities.html', {})
	
def contact(request):
	
	if request.method == "POST":
		
		html = "<p> %s </p>" % request.REQUEST.get("name")
		html += "<p> %s </p>" % request.REQUEST.get("comment")
		message = EmailMultiAlternatives("Math & Pencil Request Form", 
										 html, 
										 "noreply@mathandpencil.co,",
										 to=settings.TO_EMAIL_LIST,
										 bcc=[])
		message.attach_alternative(html , 'text/html')		
		message.send()
	
	return render(request, 'static/contact.html', {})
	
def projects(request):
	return render(request, 'static/projects.html', {})
	
def projects_1(request):
	return render(request, 'static/projects_1.html', {})
	
def projects_2(request):
	return render(request, 'static/projects_2.html', {})
	
def projects_3(request):
	return render(request, 'static/projects_3.html', {})
	
def team(request):
	return render(request, 'static/team.html', {})
	
def test(request):
	return render(request, 'static/test.html', {})
	
def websites_1(request):
	return render(request, 'static/websites_1.html', {})
	
def websites_2(request):
	return render(request, 'static/websites_2.html', {})
	
def websites_3(request):
	return render(request, 'static/websites_3.html', {})