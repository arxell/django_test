from django.conf.urls import url

from .views import statistics

urlpatterns = [
    url(r'^statistics/', statistics.view),
]
