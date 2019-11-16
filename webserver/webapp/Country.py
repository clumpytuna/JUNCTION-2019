from django.db import models


class Country(models.Model):
    """
    A country description
    """
    id = models.TextField(primary_key=True)
    name = models.TextField(null=False)
