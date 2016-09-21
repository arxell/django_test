from django.conf import settings
from django.http import HttpResponse
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader


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
