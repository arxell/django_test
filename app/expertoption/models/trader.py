from django.db import models

from app.utils import ZERO


class Trader(models.Model):

    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=ZERO)

    def __str__(self):
        return '{name}'.format(name=self.name)
