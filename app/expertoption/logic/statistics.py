import datetime as dt

from django.conf import settings
from django.db.models import Sum
from memoize import memoize

from app.expertoption.models import Deal, Transaction
from app.utils import timeit, ZERO, humanize


@timeit
@memoize(settings.CACHE_TIME)
def _get_history_deposit_data(table_date):
    deposit_data = Transaction.objects.filter(
        created_at__lt=table_date,
        type=Transaction.TRANSACTION_TYPE_DEPOSIT
    ).values('trader_id').annotate(sum=Sum('amount'))
    return {data['trader_id']: data['sum'] for data in deposit_data}


@timeit
@memoize(settings.CACHE_TIME)
def _get_history_deals_data(table_date):
    deals_data = Deal.objects.filter(
        created_at__lt=table_date,
    ).values('trader_id').annotate(sum_result_amount=Sum('result_amount'))
    return {data['trader_id']: data['sum_result_amount'] for data in deals_data}


@timeit
def get_statistics_table_context(table_date, limit=None):
    next_day = table_date + dt.timedelta(days=1)

    # fetch history deals and transactions
    history_deals_data = _get_history_deals_data(table_date)
    history_deposit_data = _get_history_deposit_data(table_date)

    # fetch today deals
    today_deals_data = Deal.objects.filter(
        created_at__range=(table_date, next_day),
    ).values('trader_id', 'trader__name', 'trader__balance').annotate(
        sum_amount=Sum('amount'),
        sum_result_amount=Sum('result_amount'),
    )
    if limit:
        today_deals_data = today_deals_data[:limit]

    # fetch today transactions
    today_deposit_data = Transaction.objects.filter(
        type=Transaction.TRANSACTION_TYPE_DEPOSIT,
        created_at__range=(table_date, next_day),
    ).values_list('trader_id').annotate(sum_amount=Sum('amount'))
    today_deposit_data = dict(today_deposit_data)

    table_data = []
    trading_volume = ZERO
    trading_result = ZERO
    today_deals_number = 0

    # build table context
    for data in today_deals_data:
        trader_id = data['trader_id']
        trading_volume += data['sum_amount']
        trading_result += data['sum_result_amount']
        today_deals_number += 1

        table_data.append(
            {
                'id': trader_id,
                'name': data['trader__name'],
                'today_profit': humanize(data['sum_result_amount']),
                'total_profit': humanize(
                    history_deals_data.get(trader_id, ZERO) +
                    data['sum_result_amount']
                ),
                'total_deposit': humanize(
                    history_deposit_data.get(trader_id, ZERO) +
                    today_deposit_data.get(trader_id, ZERO)
                ),
                'balance': humanize(data['trader__balance']),
            }
        )

    # build template context
    return {
        'date': table_date.strftime('%d %b %Y'),
        'table_data': table_data,
        'today_deals_count': today_deals_data,
        'today_deals_number': today_deals_number,
        'trading_result': humanize(trading_result),
        'trading_volume': humanize(trading_volume),
    }
