from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

# Create your models here.

#class DrawnShape(models.Model):
#    intensity = models.IntegerField("Expected intensity")
#    confidence = models.IntegerField("Confidence in prediction")
#    # type = Models.CharField(choices = [("CAS","casualties"),
#    #                                    ("ACT","activity")
#    geometry = JSONField("geoJSON")
#    def __str__(self):
#        return "a shape"
