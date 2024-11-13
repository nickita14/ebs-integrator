from collections import defaultdict
from datetime import timedelta
from functools import partial

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction, IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import last_modified
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiResponse
from drf_standardized_errors.openapi_validation_errors import extend_validation_errors
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from main.utils.view import AuthenticatedRestView, AuthenticatedModelViewSet, get_last_modified
from main.openapi import FieldValidationError
from .models import Category, Product, ProductPrice
from .serializers.model import CategorySerializer, ProductSerializer, ProductPriceSerializer
from .serializers.request import AveragePriceRequestSerializer, CategoryPriceRequestSerializer
from .serializers.response import AveragePriceResponseSerializer


@extend_schema(tags=['Categoriy'])
class CategoryViewSet(AuthenticatedModelViewSet):
    """
    The ModelViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(last_modified(partial(get_last_modified, model=Category)))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(last_modified(partial(get_last_modified, model=Category)))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=['Product'])
class ProductViewSet(AuthenticatedModelViewSet):
    """
    The ModelViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(last_modified(partial(get_last_modified, model=Product)))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(last_modified(partial(get_last_modified, model=Product)))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=['Price'])
@extend_validation_errors(
    error_codes=[FieldValidationError.END_DATE_AFTER_START_DATE.value[0]],
    field_name='end_date',
    methods=['post'],
)
@extend_validation_errors(
    error_codes=[FieldValidationError.PRODUCT_UNIQUE_TOGETHER.value[0]],
    field_name='product',
    methods=['post'],
)
class ProductPriceView(AuthenticatedRestView):

    @extend_schema(
        operation_id='addProductPrice',
        summary='Add Product Price',
        description='Set a price for a specific product over a specified date range.',
        request=ProductPriceSerializer,
        responses={
            201: ProductPriceSerializer,
        },
    )
    def post(self, request: Request, product_id: int):
        serializer = ProductPriceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, pk=product_id)

        try:
            serializer.save(product=product)
        except DjangoValidationError as e:
            errors = defaultdict(list)
            errors['end_date'].append(FieldValidationError.END_DATE_AFTER_START_DATE.value[1])
            raise DRFValidationError(errors) from e
        except IntegrityError as e:
            errors = defaultdict(list)
            errors['product'].append(FieldValidationError.PRODUCT_UNIQUE_TOGETHER.value[1])
            raise DRFValidationError(errors) from e

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Price'])
class CategoryPriceView(AuthenticatedRestView):

    @extend_schema(
        operation_id='changeCategoryPrice',
        summary='Change Category Price',
        description='Change the price for all products in a specific category.',
        request=CategoryPriceRequestSerializer,
        responses={
            204: OpenApiResponse(description='The price for all products in the category has been changed.'),
        },
    )
    def put(self, request: Request, category_id: int):
        serializer = CategoryPriceRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = get_object_or_404(Category, pk=category_id)
        product_prices = ProductPrice.objects.filter(product__category=category)

        for product_price in product_prices:
            product_price.price = serializer.validated_data['price']
            product_price.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Price'])
class AveragePriceView(AuthenticatedRestView):

    @extend_schema(
        operation_id='getCategoryAveragePrice',
        summary='Get Category Average Price',
        description='Get the average price for a specific category over a specified date range.',
        parameters=[
            OpenApiParameter(
                name='start_date',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.DATE,
                required=True,
            ),
            OpenApiParameter(
                name='end_date',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.DATE,
                required=True,
            ),
        ],
        responses={
            200: AveragePriceResponseSerializer,
            204: OpenApiResponse(description='No products found for the specified date range.'),
        },
    )
    def get(self, request: Request, category_id: int):
        category = get_object_or_404(Category, pk=category_id)

        serializer = AveragePriceRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        prices = ProductPrice.objects.filter(
            product__category=category,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        if not prices.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)

        average_price = prices.aggregate(avg_price=Avg('price'))['avg_price']

        return Response({"average_price": round(average_price, 2)}, status=status.HTTP_200_OK)
