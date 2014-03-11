from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
	url(r'^$', 								'apps.static.views.index',			name='index'),
	url(r'^about$', 						'apps.static.views.about',			name='about'),
	url(r'^projects$', 						'apps.static.views.projects',		name='projects'),
	url(r'^team$', 							'apps.static.views.team',			name='team'),
	url(r'^test$', 							'apps.static.views.test',			name='test'),
	
	url(r'^projects/3$', 					'apps.static.views.projects_2',		name='projects_2'),
	url(r'^projects/2$', 					'apps.static.views.projects_3',		name='projects_3'),
	url(r'^projects/kearney$', 				'apps.static.views.projects_1',		name='projects_1'),
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