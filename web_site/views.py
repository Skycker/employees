# coding: utf-8
import itertools

from django.shortcuts import get_object_or_404
from django.views import generic
from web_site import filters
from web_site import models


class EmployeesView(generic.ListView):
    template_name = 'web_site/list.html'
    context_object_name = 'employees'
    model = models.Employee
    paginate_by = 10
    paginate_orphans = 1

    def get_queryset(self):
        qs = self.model.objects.all().select_related()
        self.employee_filter = filters.EmployeeFilter(self.request.GET, queryset=qs)
        return self.employee_filter.qs

    def get_context_data(self, **kwargs):
        cd = super(EmployeesView, self).get_context_data(**kwargs)
        cd['departments'] = models.Department.objects.all()
        cd['current_department'] = self.employee_filter.data.get("department", None)
        cd['is_working'] = bool(self.employee_filter.data.get("is_working", None))
        return cd


class EmployeeView(generic.DetailView):
    template_name = 'web_site/detail.html'
    context_object_name = 'employee'
    model = models.Employee

    def get_object(self, queryset=None):
        return get_object_or_404(self.model.objects.select_related(), pk=self.kwargs.get('pk'))


class AlphabetEmployeesView(generic.ListView):
    template_name = 'web_site/alphabet_list.html'
    context_object_name = 'employees'
    model = models.Employee
    max_group_num = 7

    def make_groups(self):
        """ Группирует сотрудников на группы по первым буквам их фамилий
        Алгоритм:
            1. Группируем всех сотрудников по первым буквам из фамилий, все фамилии группы начинаются на одну букву
            2. Если групп не больше заданного числа, то выходим
            3. Находим группу с наименьшей длиной
            4. Объединяем ее с наименьшей группой-соседкой (справа или слева)
            5. Повторять 3 - 4 пока кол-во групп больше заданного

        """
        grouped_by_first_letter = itertools.groupby(self.model.objects.all(), lambda e: e.surname[0])
        groups = [list(employees) for _, employees in grouped_by_first_letter]
        return self.combine_min(groups, self.max_group_num)

    def combine_min(self, groups, limit):
        if len(groups) <= limit:
            return groups
        lengths = [len(g) for g in groups]
        # ищем самую маленькую группу
        smallest_index = lengths.index(min(lengths))
        # определяем, какой из ее соседей меньше
        left_index, right_index = smallest_index - 1, smallest_index + 1
        if left_index < 0 or right_index >= len(groups):
            neighbor_index = right_index if left_index < 0 else left_index
        else:
            left_len = len(groups[left_index])
            right_len = len(groups[right_index])
            neighbor_index = right_index if right_len < left_len else left_index
        # аккуратно извлекаем и объединяем выбранные группы
        index_to_extract = min([smallest_index, neighbor_index])
        combined = groups.pop(index_to_extract) + groups.pop(index_to_extract)
        groups.insert(min(smallest_index, neighbor_index), combined)
        return self.combine_min(groups, limit)

    def get_context_data(self, **kwargs):
        cd = super(AlphabetEmployeesView, self).get_context_data(**kwargs)
        groups = self.make_groups()
        groups = [{'first_letter': g[0].surname[0], 'last_letter': g[-1].surname[0], 'employees': g} for g in groups]
        cd['groups'] = sorted(groups, key=lambda x: x.get('first_letter'))
        return cd
