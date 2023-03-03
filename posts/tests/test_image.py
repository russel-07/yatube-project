from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Post, Group
from posts.forms import PostForm

User = get_user_model()


class PostTests(TestCase):
    def _get_urls(self, post, group):
        urls = [
            #reverse('index'),
            reverse('profile', kwargs={'username': post.author}),
            reverse('post', kwargs={'username': post.author, 'post_id': post.id}),
            reverse('group', kwargs={'slug': group.slug})
            ]
        return urls
    
    def _check_post_on_pages(self, post, group, text):
        urls = self._get_urls(post, group)
        for url in urls:
            response = self.client.get(url)
            print('>>>')
            print(response)
            print('<<<')

            self.assertContains(response, text, msg_prefix=f'На странице yatube.com{url} неправильно отображается запись')

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='test_user', password='test_password')
        self.client.force_login(self.test_user)

        name_test_group = 'Тестовая группа'
        self.test_group = Group.objects.create(title=name_test_group, slug='test_group')

        self.new_text = 'Тестовый пост'
        self.test_new_post = Post.objects.create(text=self.new_text, author=self.test_user, group=self.test_group)

        with open('media/posts/image.jpg','rb') as img:
            self.client.post(reverse('post_edit', kwargs={'username': self.test_user, 'post_id': self.test_new_post.id}), {'text': self.new_text, 'group': self.test_group.id, 'image': img}, follow=True)

    def testImgOnPage(self):
        teg_img = 'img class'
        self._check_post_on_pages(self.test_new_post, self.test_group, teg_img)

    def testImgWrongFormat(self):
        with open('media/posts/image.jpg','rb') as img:
            response = self.client.post(reverse('post_edit', kwargs={'username': self.test_user, 'post_id': self.test_new_post.id}), {'text': self.new_text, 'group': self.test_group.id, 'image': img}, follow=True)
            self.assertFormError(response, 'form', 'image', 'Неверный формат картинки')



 


    
