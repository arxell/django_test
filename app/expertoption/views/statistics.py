import datetime as dt

from django.http.response import HttpResponseBadRequest

from schematics import types as t
from schematics.models import Model
from schematics.exceptions import ModelConversionError, ValidationError

from app import template
from app.expertoption.logic.statistics import get_statistics_table_context
from app.utils import timeit


class StatisticsDataIn(Model):
    day = t.DateType(default=None)
    limit = t.IntType(default=None, min_value=0)

    def validate(self, *args, **kwargs):
        super().validate(*args, **kwargs)
        if not self.day:
            self.day = dt.date.today()


@timeit
def view(request):
    """
    View for /expertoption/statistics/

    Examples:
        /expertoption/statistics/
        /expertoption/statistics/?limit=10
        /expertoption/statistics/?day=2016-08-25
        /expertoption/statistics/?limit=10&day=2016-08-25
    """
    try:
        statistics_data_in = StatisticsDataIn(request.GET.dict(), strict=False)
        statistics_data_in.validate()
    except (ValidationError, ModelConversionError):
        return HttpResponseBadRequest('invalid request data')

    context = get_statistics_table_context(
        statistics_data_in.day,
        limit=statistics_data_in.limit,
    )
    return template.render_to_response('table.html', **context)
