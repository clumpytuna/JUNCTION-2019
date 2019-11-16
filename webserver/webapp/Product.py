from django.db import models


class Product(models.Model):
    """
    A product the user can buy
    """
    id = models.TextField(null=False)
    id_category = models.TextField(null=False)
    id_country = models.TextField(null=False, db_index=True)
    price = models.FloatField(null=False)
    name = models.TextField(null=True, default=None)
    description = models.TextField(null=True, default=None)
