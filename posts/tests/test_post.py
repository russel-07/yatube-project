from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class PostTests(TestCase):
    def _get_urls(self, post, group):
        urls = [
            # reverse('index'),
            reverse('profile', kwargs={'username': post.author}),
            reverse('post', kwargs={'username': post.author,
                                    'post_id': post.id}),
            reverse('group', kwargs={'slug': group.slug})
            ]
        return urls

    def _check_post_on_pages(self, post, group, text):
        urls = self._get_urls(post, group)
        for url in urls:
            response = self.auth_client.get(url)
            self.assertContains(response, text,
                                msg_prefix=f'На странице yatube.com{url} '
                                'неправильно отображается запись')

    def setUp(self):
        self.unauth_client = Client()

        self.auth_client = Client()
        self.test_user = User.objects.create_user(username='test_user',
                                                  password='test_password')
        self.auth_client.force_login(self.test_user)

        name_test_group = 'Тестовая группа'
        self.test_group = Group.objects.create(title=name_test_group,
                                               slug='test_group')

        self.new_text = 'Тестовый пост'
        self.test_new_post = Post.objects.create(text=self.new_text,
                                                 author=self.test_user,
                                                 group=self.test_group)

    # Тест - неавторизованный посетитель не может опубликовать пост
    # (его редиректит на страницу входа)
    def testNotCreatePost(self):
        response = self.unauth_client.get(reverse('new_post'))
        self.assertNotEqual(response.status_code, 200,
                            msg='Неавторизованный пользователь может зайти '
                            'на страницу добавления новой записи')
        self.assertRedirects(response, '/auth/login/?next=/new/',
                             msg_prefix='Нет переадресации на страницу '
                             'регистрации для неавторизованного пользователя')

    # Тест - авторизованный пользователь может опубликовать пост (new)
    def testCreatePost(self):
        response = self.auth_client.get(reverse('new_post'))
        self.assertEqual(response.status_code, 200,
                         msg='Авторизованный пользователь не может зайти '
                         'на страницу добавления новой записи')

        response = self.auth_client.get(
            reverse('post', kwargs={'username': self.test_user,
                                    'post_id': self.test_new_post.id})
            )
        self.assertEqual(response.status_code, 200,
                         msg='Страница новой записи недоступна')

    # Тест - после публикации поста новая запись появляется на главной
    # странице сайта (index), на персональной странице пользователя (profile),
    # и на отдельной странице поста (post)
    def testViewPost(self):
        self._check_post_on_pages(self.test_new_post, self.test_group,
                                  self.new_text)

    # Тест - авторизованный пользователь может отредактировать свой пост и
    # его содержимое изменится на всех связанных страницах
    def testEditPost(self):
        edit_text = 'Измененный пост'
        self.auth_client.post(
            reverse('post_edit', kwargs={'username': self.test_user,
                                         'post_id': self.test_new_post.id}),
            {'text': edit_text, 'group': self.test_group.id}, follow=True
            )

        self._check_post_on_pages(self.test_new_post, self.test_group,
                                  edit_text)

    # После регистрации пользователя создается его персональная страница
    def testProfilePage(self):
        response = self.auth_client.get(
            reverse('profile', kwargs={'username': self.test_user})
            )
        self.assertEqual(response.status_code, 200,
                         msg='Страница с новым пользователем недоступна')
        self.assertEqual(len(response.context["paginator"].object_list), 1,
                         msg='На странице пользователя неверное'
                         ' количество записей')
        self.assertIsInstance(response.context["author"], User,
                              msg='На страницу неверно передаются'
                              ' данные о пользователе')
        self.assertEqual(response.context["author"].username,
                         self.test_user.username,
                         msg='На странице неверное имя пользователя')
