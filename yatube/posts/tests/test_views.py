from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='HasNoName',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Текст',
            group=cls.group,
            author=cls.author,
        )

    def setUp(self):
        # self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list', kwargs={'slug': 'group-slug'}),
            'posts/post_detail.html': reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
            'posts/create_post.html': reverse('posts:create_post'),
            'posts/profile.html': reverse('posts:profile', args={self.author}),
            'posts/create_post.html': reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_group_list_page_show_correct_context(self):
        response = (self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'group-slug'})))
        self.assertEqual(response.context.get(
            'group').title, 'Тестовая группа')
        # self.assertEqual(response.context.get('posts').text, 'Тестовый текст')
        self.assertEqual(response.context.get('group').slug, 'group-slug')


class PaginatorViewsTest(TestCase):
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
        number_of_posts = 13
        for post_id in range(number_of_posts):
            Post.objects.create(text='Текст'.format(
                post_id), author=cls.author, group=cls.group)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_index_first_page_contains_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page_contains_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_first_page_contains_ten_records(self):
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': 'group-slug'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_list_second_page_contains_three_records(self):
        response = self.client.get(reverse('posts:group_list', kwargs={
                                   'slug': 'group-slug'}) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains(self):
        response = self.client.get(
            reverse('posts:profile', args={self.author}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page_contains(self):
        response = self.client.get(
            reverse('posts:profile', args={self.author}) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 3)
