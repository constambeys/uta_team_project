from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Student(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    name = models.CharField(max_length=100)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Instructor(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    department = models.CharField(max_length=100)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username