from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^create$', views.create),
    url(r'^add$', views.add),
    url(r'^favorited/(?P<itemid>\d+)$', views.favorited),
    url(r'^wish_items/(?P<itemid>\d+)$', views.wish_items),
    url(r'^remove/(?P<itemid>\d+)$', views.remove),
    url(r'^delete/(?P<itemid>\d+)$', views.delete),
]
