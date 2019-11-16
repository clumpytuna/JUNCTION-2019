from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
# Create your models here.


class JUser(User):
    categories_of_interest = ArrayField(models.TextField())
    residence = models.TextField()

