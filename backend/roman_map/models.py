from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

# Create your models here.

class CustomUser(AbstractUser):

    tanulo = models.BooleanField(default=False)
    tanar = models.BooleanField(default=False)

    def __str__(self):
        return self.last_name + ' ' + self.first_name
    

class Territorie(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    start_date = models.IntegerField()
    end_date = models.IntegerField()
    color = models.CharField(max_length=10)
    coordinates = models.TextField(blank=False)

    def __str__(self):
        return str(self.id)+' '+self.name+str(self.start_date)+' '+str(self.end_date)

class Historie(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    HISTORIE_TYPE_CHOICHES = [
        ('csata','csata'),
        ('esemeny', 'esemény'),
    ]
    historie_type = models.CharField(max_length=255, choices=HISTORIE_TYPE_CHOICHES)
    image = models.ImageField(upload_to='historie/', default=None)
    date = models.IntegerField(default=1000)
    coordinates = models.TextField(blank=False)

    def __str__(self):
        return str(self.id)+' '+self.name+' '+self.historie_type

@receiver(post_delete, sender=Historie)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class CustomPolygon(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    coordinates = models.TextField(blank=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+' '+self.name+' '+self.created_by.last_name+' '+self.created_by.first_name

class CustomPoint(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    coordinates = models.TextField(blank=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+' '+self.name+' '+self.created_by.last_name+' '+self.created_by.first_name

class CustomDraw(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    coordinates = models.TextField(blank=False)
    TYPE_CHOICHES = [
        ("point","Point"),
        ("linestring", "LineString"),
        ("polygon", "Polygon"),
        
    ]
    type = models.CharField(max_length=255, blank=False, choices=TYPE_CHOICHES)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+' '+self.name+' '+self.created_by.last_name+' '+self.created_by.first_name