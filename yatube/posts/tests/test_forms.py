from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post
from posts.forms import PostForm

User = get_user_model()


class PostModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='HasNoName'
        )
        Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            pk=1,
        )
        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.authorized_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, '/profile/HasNoName/')

    def test_edit_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=([1])),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response, '/posts/1/')
