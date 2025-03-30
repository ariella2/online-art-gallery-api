from django.db import models 
class Artwork(models.Model): 
    title = models.CharField(max_length=255) 
    description = models.TextField() 
    artist = models.CharField(max_length=255) 
    date_created = models.DateField() 
