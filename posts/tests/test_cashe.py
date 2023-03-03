from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache

from posts.models import Post, Group

User = get_user_model()


class CashTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='test_user', password='test_password')
        self.client.force_login(self.test_user)
        self.test_group = Group.objects.create(title='Тестовая группа', slug='test_group')

        post_text_1 = 'Тестовый пост'
        self.client.post(reverse('new_post'), {'text': post_text_1, 'group': self.test_group.id}, follow=True)

    def testCash(self):
        post_text_2 = 'Проверка кэширования'
        self.client.post(reverse('new_post'), {'text': post_text_2, 'group': self.test_group.id}, follow=True)

        response = self.client.get(reverse('index'))
        self.assertNotContains(response, post_text_2, msg_prefix=f'Отсутствует кэширование на главной странице')

        cache.clear()

        response = self.client.get(reverse('index'))
        self.assertContains(response, post_text_2, msg_prefix=f'Кэширование на главной странице работает неверно')







    
