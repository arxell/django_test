import logging
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from app.expertoption.models import Trader, Deal, Transaction
from app import utils


TRAIDERS_COUNT = 1000000
TRAIDER_DEALS_COUNT = 100
TRAIDER_TRANSACTIONS_COUNT = 100

log = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        for traider_number in range(0, TRAIDERS_COUNT):
            log.debug('Traider {}'.format(traider_number))

            # create trader
            trader, _ = Trader.objects.get_or_create(
                name=utils.random_string(10),
            )

            # create trader deals
            deals = []
            deal_amounts = []
            for deal_number in range(0, TRAIDER_DEALS_COUNT):

                deal_amount = utils.random_decimal()
                deal_result_amount = deal_amount + utils.random_decimal()

                deal = Deal(
                    trader=trader,
                    amount=deal_amount,
                    result_amount=deal_result_amount,
                    created_at=utils.random_date()
                )
                deals.append(deal)
                deal_amounts.append(deal_result_amount)

            # create trader transactions
            transactions = []
            transaction_amounts = []
            for deal_number in range(0, TRAIDER_TRANSACTIONS_COUNT):

                _transaction = Transaction(
                    trader=trader,
                    amount=utils.random_positive_decimal(),
                    type=random.choice([
                        Transaction.TRANSACTION_TYPE_DEPOSIT,
                        Transaction.TRANSACTION_TYPE_WITHDRAWAL,
                    ]),
                    created_at=utils.random_date(),
                )
                transactions.append(_transaction)
                if _transaction.is_type_deposit():
                    transaction_amounts.append(_transaction.amount)
                else:
                    transaction_amounts.append(_transaction.amount * (-1))

            Deal.objects.bulk_create(deals)
            Transaction.objects.bulk_create(transactions)

            # update trader balance by deal_amounts and transaction_amounts
            trader.balance = sum(deal_amounts) + sum(transaction_amounts)
            trader.save(update_fields=['balance'])
