# coding: utf-8
from django.contrib import admin

from web_site import models


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'department', 'position', 'job_start_date', 'job_end_date')
    list_filter = ('department',)


admin.site.register(models.Department)
