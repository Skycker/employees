# coding: utf-8
import django_filters

from web_site import models


class EmployeeFilter(django_filters.FilterSet):
    is_working = django_filters.CharFilter(method="filter_is_working")

    def filter_is_working(self, qs, name, value):
        return qs.filter(job_end_date__isnull=True)

    class Meta:
        model = models.Employee
        fields = ['department']
