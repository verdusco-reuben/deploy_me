from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'logout', views.logout),
    url(r'poke/(?P<id>\d+)$', views.poke)

]