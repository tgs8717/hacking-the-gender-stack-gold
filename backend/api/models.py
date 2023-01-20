from django.db import models
from django.contrib.auth.models import User


class Core(models.Model):
    smiles = models.TextField(null=False, unique=True)
    rgroup_labels = models.TextField(null=False)


class RGroup(models.Model):
    smiles = models.TextField(null=False, unique=True)


class CompoundRepo(models.Model):
    # modify contents here to whatever you want to save in the database
    smiles = models.TextField(null=False, unique=True)
    MW = models.DecimalField(null=False, decimal_places=2, max_digits=5, default=0.0)
    ALOGP = models.DecimalField(null=False, decimal_places=5, max_digits=5, default=0.0)
    HBA = models.DecimalField(null=False, decimal_places=3, max_digits=5, default=0.0)
    HBD = models.DecimalField(null=False, decimal_places=3, max_digits=5, default=0.0)
    PSA = models.DecimalField(null=False, decimal_places=2, max_digits=5, default=0.0)
    ROTB = models.DecimalField(null=False, decimal_places=2, max_digits=5, default=0.0)
    AROM = models.DecimalField(null=False, decimal_places=2, max_digits=5, default=0.0)
    ALERTS = models.DecimalField(
        null=False, decimal_places=2, max_digits=5, default=0.0
    )
    WEIGHTED_QED = models.DecimalField(
        null=False, decimal_places=5, max_digits=5, default=0.0
    )
