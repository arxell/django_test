from django.db import models

from app.utils import ZERO


class Transaction(models.Model):

    TRANSACTION_TYPE_DEPOSIT = 1
    TRANSACTION_TYPE_WITHDRAWAL = 2
    HUMAN_TRANSACTION_TYPE_DEPOSIT = 'deposit'
    HUMAN_TRANSACTION_TYPE_WITHDRAWAL = 'withdrawal'

    TRANSACTION_TYPE_CHOICES = (
        (TRANSACTION_TYPE_DEPOSIT, HUMAN_TRANSACTION_TYPE_DEPOSIT),
        (TRANSACTION_TYPE_WITHDRAWAL, HUMAN_TRANSACTION_TYPE_WITHDRAWAL),
    )

    trader = models.ForeignKey('expertoption.Trader')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=ZERO)

    type = models.IntegerField(
        choices=TRANSACTION_TYPE_CHOICES,
        default=TRANSACTION_TYPE_DEPOSIT,
        db_index=True,
    )
    created_at = models.DateTimeField(db_index=True)

    def is_type_deposit(self):
        return self.type == self.TRANSACTION_TYPE_DEPOSIT

    def is_type_withdrawal(self):
        return self.type == self.TRANSACTION_TYPE_WITHDRAWAL

    def __str__(self):
        return '{trader} {amount}'.format(
            trader=self.trader_id,
            amount=self.amount
        )

