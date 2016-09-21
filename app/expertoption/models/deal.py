from django.db import models

from app.utils import ZERO


class Deal(models.Model):

    trader = models.ForeignKey('expertoption.Trader')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=ZERO)
    result_amount = models.DecimalField(max_digits=10, decimal_places=2, default=ZERO)
    created_at = models.DateTimeField(db_index=True)

    def __str__(self):
        return '{trader} {amount}'.format(
            trader=self.trader_id,
            amount=self.amount
        )
