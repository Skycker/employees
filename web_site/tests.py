# coding: utf-8
from django.test import TestCase, Client


class EmployeeListViewTests(TestCase):
    """ Тестирование страницы списка сотрудников """

    fixtures = ['employees.json']

    def setUp(self):
        self.client = Client()

    def test_availability(self):
        """ Тест на работоспособность страницы """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('employees' in response.context, True)
        self.assertEqual('departments' in response.context, True)

    def test_filter_by_department(self):
        """ Проверка фильтрации по отделу """

        department_pk = 1
        response = self.client.get('/', {'department': department_pk})
        # правильная фильтрация
        departments_pks = [e.department_id for e in response.context['employees']]
        self.assertEqual(all([pk == department_pk for pk in departments_pks]), True)
        # текущий отдел есть в контексте
        self.assertEqual(response.context['current_department'], unicode(department_pk))

    def test_filter_by_working_now(self):
        """ Проверка фильтра 'работает сейчас' """

        response = self.client.get('/', {'is_working': True})
        # правильная фильтрация
        finish_dates = [e.job_end_date for e in response.context['employees']]
        self.assertEqual(all([d is None for d in finish_dates]), True)
        # в контексте есть соотв. флаг
        self.assertEqual(response.context['is_working'], True)


class AlphabetEmployeeListViewTests(TestCase):
    """ Тестирование алфавитного указателя по сотрудникам """

    fixtures = ['employees.json']
    max_alphabet_group_num = 7

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/alphabet-employees/')

    def test_availability(self):
        """ Тест на работоспособность страницы """

        self.assertEqual(self.response.status_code, 200)
        self.assertEqual('groups' in self.response.context, True)

    def test_group_len(self):
        """ Проверка количества групп на странице """

        self.assertEqual(len(self.response.context['groups']) <= self.max_alphabet_group_num, True)

    def test_group_content(self):
        """ Проверка того, что буквы в группах не пересекаются """

        groups = self.response.context['groups']
        letters = []
        for g in groups:
            first_letter = g['first_letter']
            last_letter = g['last_letter']
            letters.append(first_letter)
            if first_letter != last_letter:
                letters.append(last_letter)
        self.assertEqual(len(letters) == len(set(letters)), True)





