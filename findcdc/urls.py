from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from .views import  HomePageView
from search import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'findcdc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^registration/$', views.cdc_reg, name='cdc_registration'),
    url(r'^d/(?P<center_id>\w+)/$',views.get_center_detail,name='center_details_view'),
    url(r'^report/(?P<center_id>\w+)/$',views.report_abuse,name='report_abuse_view'),
    url(r'^start/$', views.tool_functionality, name='functionality'),
    url(r'^tips/$', views.prevention_tips, name='ebola_tips'),
    url(r'^contact/$', views.contact_us, name='contact'),
    url(r'^about/$', views.about_us, name='about'),
   	url(r'^search/$',views.search_view,name='search_view'),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),

)
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
)
