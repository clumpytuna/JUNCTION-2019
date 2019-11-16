from django.conf.urls import url

from webapp.views_trip import trip_step, trip_get
from webapp.views import IndexView


urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^step$', trip_step),
    url(r'^trip$', trip_get),
]
