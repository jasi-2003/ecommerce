from django.db import models

from django.contrib.auth.models import User

# Create your models here.





# pyhton manage.py createsuperuser
   
#email:
#password:




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Location Fields
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.DecimalField(max_digits=9,decimal_places=0,  blank=True, null=True)
    

    def __str__(self):
        return self.user.username
