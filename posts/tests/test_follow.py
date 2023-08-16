from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Post, Group, Comment

User = get_user_model()


class FollowTests(TestCase):
    def _get_urls(self, post, group):
        urls = [
            reverse('index'),
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
                                f'неправильно отображается запись')

    def setUp(self):
        self.client = Client()
        self.following_user = User.objects.create_user(
            username='following_user', password='test_password'
            )
        self.follower_user = User.objects.create_user(
            username='follower_user', password='test_password'
            )
        self.not_follower_user = User.objects.create_user(
            username='not_follower_user', password='test_password'
            )

        self.new_text = 'Тестовый пост'
        self.test_group = Group.objects.create(
            title='Тестовая группа', slug='test_group'
            )
        self.test_post = Post.objects.create(
            text=self.new_text, author=self.following_user,
            group=self.test_group
            )

    # Тест - авторизованный пользователь может подписываться
    # на других пользователей и удалять их из подписок
    def testAddFollowing(self):
        self.client.force_login(self.follower_user)
        response = self.client.post(
            reverse('profile_follow',
                    kwargs={'username': self.following_user}),
            follow=True
        )
        self.assertRedirects(response, f'/{self.following_user}/',
                             msg_prefix='Нет переадресации на '
                             'страницу подписываемого автора')
        self.assertEqual(response.context["author"].following.count(),
                         1, msg='Неверно отображается количество подписчиков')
        self.assertContains(response, 'Подписчиков: 1',
                            msg_prefix='На странице автора неверно '
                            'отображается количество подписчиков')

        response = self.client.get(
            reverse('profile', kwargs={'username': self.follower_user}),
            follow=True
            )
        self.assertEqual(response.context["author"].follower.count(),
                         1, msg='Неверно отображается количество подписок')
        self.assertContains(response, 'Подписан: 1',
                            msg_prefix='На странице профайла неверно '
                            'отображается количество подписок')

        response = self.client.post(
            reverse('profile_unfollow',
                    kwargs={'username': self.following_user}),
            follow=True
            )
        self.assertRedirects(response, f'/{self.following_user}/',
                             msg_prefix='Нет переадресации на '
                             'страницу отписываемого автора')
        self.assertEqual(response.context["author"].following.count(),
                         0, msg='Неверно отображается количество подписчиков')
        self.assertContains(response, 'Подписчиков: 0',
                            msg_prefix='На странице автора неверно '
                            'отображается количество подписчиков')

        response = self.client.get(
            reverse('profile', kwargs={'username': self.follower_user}),
            follow=True
            )
        self.assertEqual(response.context["author"].follower.count(), 0,
                         msg='Неверно отображается количество подписок')
        self.assertContains(response, 'Подписан: 0',
                            msg_prefix='На странице профайла неверно '
                            'отображается количество подписок')

    # Тест - новая запись пользователя появляется в ленте тех, кто на него
    # подписан и не появляется в ленте тех, кто не подписан на него
    def testFollowerFeed(self):
        self.client.force_login(self.follower_user)
        self.client.post(
            reverse('profile_follow',
                    kwargs={'username': self.following_user}),
            follow=True
            )
        response = self.client.get(reverse('follow_index'))
        self.assertIn(self.test_post,
                      response.context['paginator'].object_list,
                      msg='В ленте подписчика нет записи подписанного автора')
        self.assertContains(response, self.new_text,
                            msg_prefix='В ленте подписчика не отображается '
                            'запись подписанного автора')

        self.client.force_login(self.not_follower_user)
        response = self.client.get(reverse('follow_index'))
        self.assertNotIn(self.test_post,
                         response.context['paginator'].object_list,
                         msg='В ленте появляется запись '
                         'неподписанного автора')
        self.assertNotContains(response, self.new_text,
                               msg_prefix='В ленте отображается запись '
                               'неподписанного автора')

    # Тест - только авторизированный пользователь может комментировать посты
    def testPostComment(self):
        test_comment_text = ('Тестовый комментарий от '
                             'неавторизованного пользователя')
        response = self.client.post(
            reverse('add_comment',
                    kwargs={'username': self.following_user,
                            'post_id': self.test_post.id}),
            {'text': test_comment_text}, follow=True
            )
        test_comment = Comment.objects.filter(text=test_comment_text,
                                              author=self.follower_user,
                                              post=self.test_post)
        self.assertRedirects(
            response, '/auth/login/?next=%2Ffollowing_user%2F1%2Fcomment%2F',
            msg_prefix='Нет переадресации на страницу авторизации'
            )
        response = self.client.get(
            reverse('post', kwargs={'username': self.following_user,
                                    'post_id': self.test_post.id})
            )
        self.assertNotContains(
            response, test_comment_text,
            msg_prefix=('На странице поста отображается комментарий '
                        'от неавторизованного пользователя')
            )

        test_comment_text = ('Тестовый комментарий от '
                             'авторизованного пользователя')
        self.client.force_login(self.follower_user)
        response = self.client.post(
            reverse('add_comment',
                    kwargs={'username': self.following_user,
                            'post_id': self.test_post.id}),
            {'text': test_comment_text}, follow=True
            )
        test_comment = Comment.objects.get(text=test_comment_text,
                                           author=self.follower_user,
                                           post=self.test_post)
        self.assertRedirects(
            response, f'/{self.following_user}/{self.test_post.id}/',
            msg_prefix='Нет переадресации на страницу комментируемого поста')
        self.assertIn(test_comment, response.context['comments'],
                      msg='На странице поста нет комментария')
        self.assertContains(response, test_comment_text,
                            msg_prefix=('На странице поста не '
                                        'отображается комментарий'))
