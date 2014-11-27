from django.conf.urls import patterns, include, url

from django.contrib.auth.views import login

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # AUTHENTICATION URLS
    url(r'^login/', ('user_account.views.login')),
     url(r'^error/', ('user_account.views.invalid_login')),
    url(r'^logout/', ('user_account.views.logout')),
    url(r'^auth/', ('user_account.views.auth_view')),

    # REGISTRATION URLS
    url(r'^create-account/', ('user_account.views.register_user')),
    url(r'^account-successfully-created/', ('user_account.views.register_success')),
    url(r'^submit/(?P<activation_key>\w+)/', ('user_account.views.register_confirm')),
    

    # PASWORD CHANGING AND RESETING
    url(r'^password-forgot/', ('user_account.views.forgot_password')),
    url(r'^password-change-successfull/$', 'django.contrib.auth.views.password_change_done', 
        {'template_name': 'user_account/password_change_done.html'}),
    url(r'^change-password/$', 'django.contrib.auth.views.password_change', 
        {'template_name': 'user_account/password_change.html',
        'post_change_redirect': '/user-account/password-change-successfull'}),

    url(r'^password/reset/$', 'user_account.views.password_reset',
        {'template_name': 'user_account/password_reset_form.html',
        'email_template_name': 'user_account/password_reset_email.html', 
        'subject_template_name':'user_account/password_reset_subject.txt',
        'post_reset_redirect' : '/user-account/password/reset/successfull/'}, 
        ),
    url(r'^password/reset/successfull/$', 'django.contrib.auth.views.password_reset_done',
        {'template_name': 'user_account/password_reset_done.html'}),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'template_name': 'user_account/password_reset_confirm.html',
        'post_reset_redirect' : '/user_account/password/reset-successfull/'}),
    url(r'^password/reset-successfull/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'user_account/password_reset_complete.html'}),   
    
)

