from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Category, Product, ProductPrice


class CategoryViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", category=self.category, sku="SP1000")
        self.valid_payload = {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'price': '999.99'
        }

    def test_list_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Category.objects.count())

    def test_retrieve_category(self):
        response = self.client.get(reverse('category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)


class ProductViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", category=self.category, sku="SP1000")

    def test_list_products(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())

    def test_retrieve_product(self):
        response = self.client.get(reverse('product-detail', args=[self.product.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)


class ProductPriceViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(name="Smartphone", category=self.category, sku="SP1000")
        self.valid_payload = {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'price': '999.99'
        }

    def test_create_product_price(self):
        response = self.client.post(
            reverse('product-price', args=[self.product.id]),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductPrice.objects.count(), 1)

    def test_create_product_price_invalid_date(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['end_date'] = '2022-12-31'  # End date before start date
        response = self.client.post(
            reverse('product-price', args=[self.product.id]),
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CategoryPriceViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Electronics")
        self.product1 = Product.objects.create(name="Smartphone", category=self.category, sku="SP1000")
        self.product2 = Product.objects.create(name="Laptop", category=self.category, sku="LT2000")
        ProductPrice.objects.create(product=self.product1, start_date=date(2023, 1, 1), end_date=date(2023, 12, 31), price=1000)
        ProductPrice.objects.create(product=self.product2, start_date=date(2023, 1, 1), end_date=date(2023, 12, 31), price=1500)
        self.valid_payload = {'price': '1200.00'}

    def test_update_category_price(self):
        response = self.client.put(
            reverse('category-price', args=[self.category.id]),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that all products in the category have the updated price
        for product_price in ProductPrice.objects.filter(product__category=self.category):
            self.assertEqual(product_price.price, 1200)


class AveragePriceViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Electronics")
        self.product1 = Product.objects.create(name="Smartphone", category=self.category, sku="SP1000")
        self.product2 = Product.objects.create(name="Laptop", category=self.category, sku="LT2000")
        ProductPrice.objects.create(product=self.product1, start_date=date(2023, 1, 1), end_date=date(2023, 12, 31), price=1000)
        ProductPrice.objects.create(product=self.product2, start_date=date(2023, 1, 1), end_date=date(2023, 12, 31), price=1500)

    def test_average_price(self):
        response = self.client.get(
            reverse('average-price', args=[self.category.id]),
            {'start_date': '2023-01-01', 'end_date': '2023-12-31'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['average_price'], 1250.00, places=2)

    def test_average_price_no_prices(self):
        empty_category = Category.objects.create(name="Empty Category")
        response = self.client.get(
            reverse('average-price', args=[empty_category.id]),
            {'start_date': '2023-01-01', 'end_date': '2023-12-31'}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
