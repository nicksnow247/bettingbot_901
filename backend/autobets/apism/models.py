from django.db import models
# Create your models here.
class SessionToken(models.Model):
    
    token = models.CharField(null=True, max_length=100)
    
