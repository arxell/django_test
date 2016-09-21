from decimal import Decimal, ROUND_HALF_UP
import datetime as dt
import logging
import random
import string
import time

from django.conf import settings
from django.http import HttpResponse
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

TWO_PLACES = Decimal('0.01')
ZERO = Decimal('0')

log = logging.getLogger(__name__)


def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_decimal():
    return Decimal(random.uniform(-10000.10, 10000.10))


def random_positive_decimal():
    return Decimal(random.uniform(1, 10000.10))


def random_date():
    now = dt.date.today()
    now -= dt.timedelta(days=random.randrange(0, 30))
    return now


def to_decimal(s):
    return Decimal(str(s))


def two_places(d):
    return d.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def humanize(d):
    if d > ZERO:
        return '+${:,}'.format(two_places(to_decimal(d)))
    else:
        d *= -1
        return '-${:,}'.format(two_places(to_decimal(d)))


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        log.debug('{method} {time} (sec)'.format(
            method=method.__name__,
            time=te - ts)
        )
        return result

    return timed


env = Environment(
    loader=FileSystemLoader(settings.JINJA2_TEMPLATE_DIRS),
    autoescape=True,
    extensions=['jinja2.ext.i18n'],
)
env.install_null_translations()


def render_to_response(template_name, **context):
    return HttpResponse(
        env.get_template(template_name).render(context),
        content_type='text/html'
    )
