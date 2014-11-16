from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	url(r'^profile/(?P<username>[\w\-+.@]+)/$', 'user_profile.views.profile', name='user-profile'),

	url(r'^profile/(?P<username>[\w\-+.@]+)/update_profile/$', 
		'user_profile.views.update_profile', name='update-profile'),

	url(r'^profile/(?P<username>[\w\-+.@]+)/settings/$', 
		'user_profile.views.profile_settings', name='profile-settings'),

	url(r'^user_account/profile/(?P<username>[\w\-+.@]+)/delete-account/$', 
		'user_profile.views.delete_user', name='delete-user'),

) 