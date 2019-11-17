from django.db import models


class Product(models.Model):
    """
    A product the user can buy
    """
    id = models.TextField(primary_key=True)
    id_country = models.TextField(null=True, db_index=True)
    id_category = models.TextField(null=True, db_index=True)
    name = models.TextField(null=True, default=None)
    description = models.TextField(null=True, default=None)
    price = models.FloatField(null=True, default=None)
    link = models.TextField(null=False, default='https://google.com')
