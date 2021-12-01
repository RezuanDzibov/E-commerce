from typing import Type, Optional
from collections import OrderedDict

from django.http import HttpRequest
from rest_framework import exceptions

from src.cart.serializers import (
    CartProductItemAddSerializer,
    CartProductItemRemoveSerializer,
    CartProductItemReduceSerializer
)
from src.item.models import Item
from src.item.serializers import ItemSerializer
from src.product.models import Product
from src.core.serialize_utils import get_serializer_by_objects, get_serializer_by_data, get_validated_serializer
from src.core.exceptions import exception_raiser
from src.core.services import AbstractService


def get_cart_product_items(request: HttpRequest) -> Type[OrderedDict]:
    """
    Return product items' data from the cart of the requesting user.
    @param request: An authenticated instance of HttpRequest.
    @return: ItemSerializer's data.
    """
    product_items = request.user.cart.items.all()
    product_items_data = get_serializer_by_objects(ItemSerializer, objects=product_items, many_objects=True).data
    return product_items_data


def clear_cart(request: HttpRequest) -> None:
    """
    Clear all product items from the cart of the requesting user.
    @param request: An authenticated instance of HttpRequest.
    @return: None
    """
    request.user.cart.items.all().delete()


class AddItemToCart(AbstractService):
    """Add product item to customer cart or update of quantity product item in cart."""
    def execute(self) -> Type[OrderedDict]:
        """
        Performer method.
        @return: ItemSerializer's data.
        """
        request_data_serializer = get_validated_serializer(
            get_serializer_by_data(serializer_class=CartProductItemAddSerializer, data=self.request.data)
        )
        product = self._get_product(request_data_serializer)
        product_item = self._get_product_item(product)
        if product_item is None:
            product_item = self._create_product_item(product, request_data_serializer)
        else:
            product_item = self._update_product_item(product_item, request_data_serializer)
        return get_serializer_by_objects(serializer_class=ItemSerializer, objects=product_item).data

    def _get_product(self, request_data_serializer: CartProductItemAddSerializer) -> Optional[Product]:
        """
        Return Product item if it exists or raise exception.
        @param request_data_serializer: CartProductAddSerializer
        @return: Product model instance.
        @raise: exceptions.NotFound if product didn't find.
        """
        try:
            product = Product.objects.get(slug=request_data_serializer.data.get("product_slug"))
            return product
        except Product.DoesNotExist:
            return exception_raiser(
                exception_class=exceptions.NotFound,
                msg=f"No such product with slug {request_data_serializer.data.get('product_slug')}."
            )

    def _get_product_item(self, product: Product) -> Optional[Item]:
        """
        @param product: Product model instance.
        @return: Item model instance or None.
        """
        try:
            product_item = Item.objects.get(cart__id=self.request.user.cart.id, product=product)
            return product_item
        except Item.DoesNotExist:
            return None

    def _create_product_item(self, product: Product, request_data_serializer: CartProductItemAddSerializer) -> Item:
        """
        Create Item model instance.
        @param product: Product model instance.
        @param request_data_serializer:
        @return: Item model instance.
        """
        product_item = Item.objects.create(
            content_object=self.request.user.cart,
            product=product,
            quantity=request_data_serializer.data.get("product_qty")
        )
        return product_item

    def _update_product_item(self, product_item: Item, request_data_serializer: CartProductItemAddSerializer) -> Item:
        """
        Update Item model instance
        @param product_item: Item model instance.
        @param request_data_serializer: CartProductAddSerializer.
        @return: Item model instance.
        """
        product_item.quantity += request_data_serializer.data.get("product_qty")
        product_item.save()
        return product_item


class ReduceQuantityOfProductItem(AbstractService):
    """Reduce quantity of product item in cart."""
    def execute(self) -> Optional[Type[OrderedDict]]:
        """
        Performer method.
        @return: ItemSerializer's data.
        """
        request_data_serializer = get_validated_serializer(
            get_serializer_by_data(serializer_class=CartProductItemReduceSerializer, data=self.request.data)
        )
        product_item = self._get_product_item(request_data_serializer)
        product_item = self._reduce_quantity_of_product_item(product_item, request_data_serializer)
        if product_item.quantity == 0:
            self._delete_product_item(product_item)
            return None
        product_item = get_serializer_by_objects(serializer_class=ItemSerializer, objects=product_item).data
        return product_item

    def _get_product_item(self, request_data_serializer: CartProductItemReduceSerializer) -> Item:
        """
        @param request_data_serializer: CartProductRemoveSerializer.
        @return: Item model instance.
        """
        try:
            product_item = Item.objects.get(
                cart__id=self.request.user.cart.id,
                product__slug=request_data_serializer.data.get("product_slug")
            )
            return product_item
        except Item.DoesNotExist:
            raise exception_raiser(
                exception_class=exceptions.NotFound,
                msg=f"No such product with slug {request_data_serializer.data.get('product_slug')}."
            )

    def _reduce_quantity_of_product_item(self, product_item: Item,
                                         request_data_serializer: CartProductItemReduceSerializer) -> Item:
        """
        Reduce quantity of Item model instance by request_data_serializer its parameter product_qty.
        @param product_item: Item model instance.
        @param request_data_serializer: CartProductRemoveSerializer.
        @return: Item model instance.
        """
        product_item.quantity -= request_data_serializer.data.get("product_qty", 1)
        product_item.save()
        return product_item

    def _delete_product_item(self, product_item: Item):
        """
        Delete Item model instance.
        @param product_item: Item model instance.
        @return: None
        """
        product_item.delete()


class RemoveProductItemFromCart(ReduceQuantityOfProductItem):
    """Remove product item from customer cart."""
    def execute(self) -> None:
        """
        Performer method.
        @return: None.
        """
        request_data_serializer = get_validated_serializer(
            get_serializer_by_data(serializer_class=CartProductItemRemoveSerializer, data=self.request.data)
        )
        product_item = self._get_product_item(request_data_serializer)
        self._delete_product_item(product_item)