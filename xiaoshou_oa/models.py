#code=utf-8
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Person(models.Model):
    user=models.OneToOneField(User)
    sex=models.BooleanField(default=True, verbose_name=u'性别', help_text=u'性别')

