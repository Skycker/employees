# coding: utf-8
from django.db import models
from django.urls import reverse


class Department(models.Model):
    title = models.CharField(u'Отдел', max_length=128)

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        ordering = ('title',)


class Employee(models.Model):
    department = models.ForeignKey(Department, verbose_name=u'Отдел')
    surname = models.CharField(u'Фамилия', max_length=64)
    name = models.CharField(u'Имя', max_length=64)
    patronymic = models.CharField(u'Отчетсво', max_length=64)
    birthday = models.DateField(u'Дата рождения')
    email = models.EmailField(u'Email', blank=True, null=True)
    phone = models.CharField(u'Телефон', max_length=16, blank=True, null=True)
    job_start_date = models.DateField(u'Дата начала работы')
    job_end_date = models.DateField(u'Дата окончания работы', blank=True, null=True,
                                    help_text=u'пустая если всё ещё работает')
    position = models.CharField(u'Должность', max_length=64)

    def __unicode__(self):
        return u"{0} {1} {2}".format(self.surname, self.name, self.patronymic)

    def get_absolute_url(self):
        return reverse("web_site:employee", kwargs={'pk': self.pk})

    class Meta:
        ordering = ('surname', 'name')
