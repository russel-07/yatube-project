# coding=utf-8
from django.test import TestCase, Client
import datetime as dt

from django.contrib.auth import get_user_model

User = get_user_model()

# Тесты для проверки страницы сайта с тарифными планами.
class PlansPageTest(TestCase):
    def setUp(self):
        self.client = Client() # создание тестового клиента
        self.response = self.client.get("/plans/")


    # Тест - главная страница доступна неавторизованному пользователю, а раздел администратора — нет
    def testPageCodes(self):
        self.assertEqual(self.response.status_code, 200, msg='Страница с тарифами не найдена')
        self.response = self.client.get("/admin/")
        self.assertNotEqual(self.response.status_code, 200, msg='Страница администратора доступна неавторизованному пользователю')

    # Тест - переменная plans есть в контексте шаблона
    def testIndexContext(self):
        var = 'plans'
        self.assertIn(var, self.response.context, msg = f'Переменная {var} не найдена в контексте шаблона')
    
    # Тест - имя шаблона, который вызывается при рендеринге главной страницы — tariffs.html
    def testIndexTemplate(self):
        template_name = 'tariffs.html'
        self.assertTemplateUsed(self.response, template_name, msg_prefix = f'Имя шаблона главной страницы не {template_name}')

    # Тест - тип переменной plans — это список, состоящий из 3-х элементов, а их тип — словарь
    def testIndexPlans(self):
        self.assertIsInstance(self.response.context['plans'], list, msg='Тип переменной plans не является списком')
        self.assertEqual(len(self.response.context['plans']), 3, msg='Переменная plans состоит не из 3-х элементов')
        for i in self.response.context['plans']:
            self.assertIsInstance(i, dict, msg = f'Элемент {i} переменной plans не является словарем')

    # Тест - на результирующей странице показываются названия тарифных планов и подставляется правильная тема (subject) в ссылку на кнопке "Связаться"
    def testIndexContent(self):
        tariffs_name = ['Бесплатно', 'Профессиональный', 'Корпоративный']        
        for tariff in tariffs_name:
            text = f'mailto:order@company.site?subject={tariff}'
            self.assertContains(self.response, text, msg_prefix = f'На странице не показывается тарифный план: {tariff}')       

    # Тест - в контекстных переменных шаблона присутствует текущий год и он же правильно появляется на странице
    def testContextProcessor(self):
        today = dt.datetime.today().year
        self.assertEqual(self.response.context["year"], today, msg='В подвале страницы неверно указан текущий год')
