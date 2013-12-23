from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template import TemplateDoesNotExist
from django import http

def tm_render(request, *args, **kwargs):
	kwargs['context_instance'] = RequestContext(request)
	return render_to_response(*args, **kwargs)

		