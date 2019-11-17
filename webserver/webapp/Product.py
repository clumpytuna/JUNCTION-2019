from django.db import models


class Product(models.Model):
    """
    A product the user can buy
    """
    id = models.TextField(primary_key=True)
    id_category_in_country = models.TextField(null=False)
    name = models.TextField(null=True, default=None)
    description = models.TextField(null=True, default=None)
    price = models.FloatField(null=True, default=None)
    link = models.TextField(null=False, default='https://google.com')
