from django.db import models
import django.contrib.postgres.fields as pgmodels


class Trip(models.Model):
    """
    A trip description and results of recommendation system (JSON-encoded)
    """
    id = models.TextField(null=False)

    home_country = models.TextField(null=False, help_text='Country reference')
    interests = pgmodels.ArrayField(models.TextField(), null=False, help_text='List of Category references')

    countries = pgmodels.ArrayField(models.TextField(), null=False,
                                    help_text='List of Country references. '
                                              'Length of this field MUST be equal to length of "results"')
    results = pgmodels.ArrayField(models.TextField(), null=False, default=list,
                                  help_text='List of JSON. '
                                            'Length of this field MUST be equal to length of "countries"')
    prepared = models.BooleanField(null=False, default=False)
