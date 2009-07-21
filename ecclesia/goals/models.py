from django.db import models

# Create your models here.
class Goal(models.Model):
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name