# coding: utf-8
from django.conf.urls import url

from web_site import views

urlpatterns = [
    url(r'^$', views.EmployeesView.as_view(), name='employees'),
    url(r'^alphabet-employees/$', views.AlphabetEmployeesView.as_view(), name='alphabet-employees'),
    url(r'^employees/(?P<pk>\d+)/$', views.EmployeeView.as_view(), name='employee'),
]
