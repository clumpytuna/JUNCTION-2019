from django.db import models


class CategoryInCountry(models.Model):
    """
    A category in some Country
    """
    id = models.TextField(primary_key=True)
    id_country = models.TextField(null=False, db_index=True, help_text='Country reference')
    id_category = models.TextField(null=False, help_text='Category reference')
    price = models.FloatField(null=False)
