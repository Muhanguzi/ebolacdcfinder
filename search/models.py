from django.contrib.gis.db import models

class Services(models.Model):


	country = models.CharField(max_length= 100)
	city = models.CharField(max_length= 100)
	roadAddress = models.CharField(max_length=250)
	centerName = models.CharField(max_length = 100)
	telephone = models.CharField(max_length= 50,blank=True,null=True)
	location = models.PointField(srid=4326,blank=True,null=True)
	objects = models.GeoManager()



	def __unicode__(self):
		return unicode(self.centerName)
        
class Abuse(models.Model):

	center_id = models.IntegerField(blank=True,null=True)
	description = models.TextField(blank=True,null=True)

	def __unicode__(self):
		return unicode(self.description)

