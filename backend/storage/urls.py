from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_id>/price/', views.ProductPriceView.as_view(), name='product-price'),
    path('categories/<int:category_id>/price/', views.CategoryPriceView.as_view(), name='category-price'),
    path('categories/<int:category_id>/price/average/', views.AveragePriceView.as_view(), name='average-price'),
]
