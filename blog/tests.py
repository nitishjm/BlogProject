from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post


class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='TestUser',
            email='testuser@gmail.com',
            password='hello123'
        )

        self.post = Post.objects.create(
            title='testpost',
            author=self.user,
            body='This is a test post'
        )

    def test_string_representation(self):
        post = Post(title='testpost')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", 'testpost')
        self.assertEqual(f"{self.post.author}", 'TestUser')
        self.assertEqual(f"{self.post.body}", "This is a test post")

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'This is a test post')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'post_detail.html')
        self.assertContains(response, 'This is a test post')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'new post',
            'author': self.user,
            'body': 'sample text'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "new post")
        self.assertContains(response, "sample text")
        self.assertEqual(str(self.user), 'TestUser')

    def test_post_modify_view(self):
        response = self.client.post(reverse('post_modify', args='1'), {
            'title': "Updated title",
            'body': "Updated body"
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)