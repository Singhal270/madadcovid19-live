from django.db import models


class City(models.Model):
	name=models.CharField(max_length=200, null=True, blank=False)
	def __str__(self):
		return self.name

class Resources(models.Model):
	name=models.CharField(max_length=200, null=True, blank=False)
	def __str__(self):
		return self.name

class Supplier(models.Model):
	STATUS = (
			('helpful', 'helpful'),
			('unresponsive', 'unresponsive'),
			('out of stock', 'out of stock'),
			('wrong', 'wrong'),
			('fraud','fraud'),
			('unvarified','unvarified')
			)
	name=models.CharField(max_length=50, null=True, blank=False)
	Number=models.IntegerField(null=True,blank=False)
	status = models.CharField(max_length=200, null=True, choices=STATUS,blank=False)
	date_created=models.DateTimeField(auto_now=True, null =True)
	description=models.TextField(max_length=300,blank=False)
	email=models.EmailField(blank=True)
	city = models.ManyToManyField(City)
	resources=models.ManyToManyField(Resources)
	def __str__(self):
		return self.name

