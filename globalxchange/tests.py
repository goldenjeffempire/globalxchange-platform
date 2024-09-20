# globalxchange/tests.py

from django.test import TestCase
from django.urls import reverse
from .models import Product, Order
from django.contrib.auth.models import User

class ProductModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            price=9.99
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(str(self.product), 'Test Product')

class ProductViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            price=9.99
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
