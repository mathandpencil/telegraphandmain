from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
	url(r'^$', 'apps.static.views.index', 			name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )