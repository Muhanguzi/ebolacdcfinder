from django.contrib.gis import admin
from search.models import Services,Abuse

mymodels = [Services,Abuse]
admin.site.register(mymodels, admin.OSMGeoAdmin)