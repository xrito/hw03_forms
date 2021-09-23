from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='HasNoName'
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        # self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def post_about_page_uses_correct_template(self):
        """URL-адрес использует шаблон deals/home.html."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')



    # # Проверяем используемые шаблоны
    # def post_pages_uses_correct_template(self):
    #     """URL-адрес использует соответствующий шаблон."""
    #     # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
    #     templates_pages_names = {
    #         'posts/index.html': reverse('posts:index'),
    #         'posts/profile.html': (
    #             reverse('posts:profile', args=('username',))
    #         ),
    #         'posts/create_post.html': reverse('posts:create_post'),
    #         'posts/group_list.html': (
    #             reverse('posts:group_list', kwargs={'slug': 'group-slug'})
    #         ),
    #         'post/post_detail.html': reverse('posts:post_detail'),
    #         'posts/create_post.html': (
    #             reverse('posts:post_edit', args=('post_id',))
    #         ),
    #     }
    #     # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
    #     for template, reverse_name in templates_pages_names.items():
    #         with self.subTest(reverse_name=reverse_name):
    #             response = self.authorized_client.get(reverse_name)
    #             self.assertTemplateUsed(response, template)
