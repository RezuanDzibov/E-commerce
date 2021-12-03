from collections import OrderedDict
from typing import Type, Optional

from django.http import HttpRequest
from rest_framework import exceptions

from src.cart.serializers import CartProductItem
from src.core.exceptions import exception_raiser
from src.core.serialize_utils import (
    get_serializer_by_objects,
    get_serializer_by_data,
    get_validated_serializer,
    get_serializer_data
)
from src.core.services import BaseService
from src.item.models import Item
from src.item.serializers import ItemSerializer
from src.product.models import Product


def get_product_item(request: HttpRequest, product_slug: str) -> Optional[Item]:
    """
    @param request: Authenticated HttpRequest.
    @param product_slug: Product model instance slug.
    @return: Item model instance or None.
    """
    try:
        product_item = Item.objects.get(cart=request.user.cart, product__slug=product_slug)
        return product_item
    except Item.DoesNotExist:
        return None


def get_cart_product_items(request: HttpRequest) -> Type[OrderedDict]:
    """
    Return product items' data from the cart of the requesting user.
    @param request: Authenticated HttpRequest.
    @return: Serializer data.
    """
    product_items = request.user.cart.items.all()
    product_items_data = get_serializer_by_objects(ItemSerializer, objects=product_items, many_objects=True).data
    return product_items_data


def clear_cart(request: HttpRequest) -> None:
    """
    Clear all product items from the cart of the requesting user.
    @param request: Authenticated HttpRequest.
    @return: None
    """
    request.user.cart.items.all().delete()


class AddItemToCart(BaseService):
    """Add product item to customer cart or update of quantity product item in cart."""
    def execute(self, product_slug: str) -> Type[OrderedDict]:
        """
        Performer method.
        @param product_slug: Product model instance slug.
        @return: Serializer data.
        """
        product_item_quantity = get_validated_serializer(
            get_serializer_by_data(serializer_class=CartProductItem, data=self.request.data)
        ).data.get("product_qty", 1)
        product = self._get_product(product_slug=product_slug)
        product_item = self._get_product_item(product)
        if product_item is None:
            product_item = self._create_product_item(product=product, product_item_quantity=product_item_quantity)
        else:
            product_item = self._update_product_item(
                product_item=product_item,
                product_item_quantity=product_item_quantity
            )
        product_item = get_serializer_data(
            get_serializer_by_objects(serializer_class=ItemSerializer, objects=product_item)
        )
        return product_item

    def _get_product(self, product_slug: str) -> Optional[Product]:
        """
        Return Product item if it exists or raise exception.
        @param product_slug: Product model instance slug.
        @return: Product model instance.
        @raise: If Product model instance doesn't exist.
        """
        try:
            product = Product.objects.get(slug=product_slug)
            return product
        except Product.DoesNotExist:
            return exception_raiser(
                exception_class=exceptions.NotFound,
                msg=f"No such product with slug {product_slug}."
            )

    def _get_product_item(self, product: Product) -> Optional[Item]:
        """
        @param product: Product model instance.
        @return: Item model instance or None.
        """
        product_item = get_product_item(request=self.request, product_slug=product.slug)
        return product_item

    def _create_product_item(self, product: Product, product_item_quantity: int) -> Item:
        """
        Create Item model instance.
        @param product: Product model instance.
        @param product_item_quantity: Quantity of product on which need to reduce by default 1.
        @return: Item model instance.
        """
        product_item = Item.objects.create(
            content_object=self.request.user.cart,
            product=product,
            quantity=product_item_quantity
        )
        return product_item

    def _update_product_item(self, product_item: Item, product_item_quantity: int) -> Item:
        """
        Update Item model instance
        @param product_item: Item model instance.
        @param product_item_quantity: Quantity of product on which need to reduce by default 1.
        @return: Item model instance.
        """
        product_item.quantity += product_item_quantity
        product_item.save()
        return product_item


class ReduceQuantityOfProductItem(BaseService):
    """Reduce quantity of product item in cart."""
    def execute(self, product_slug: str) -> Optional[Type[OrderedDict]]:
        """
        Performer method.
        @param product_slug: Product model instance slug.
        @return: Serializer data.
        """
        product_item_quantity = get_validated_serializer(
            get_serializer_by_data(serializer_class=CartProductItem, data=self.request.data)
        ).data.get("product_qty", 1)
        product_item = self._get_product_item(product_slug)
        product_item = self._reduce_quantity_of_product_item(product_item, product_item_quantity)
        if product_item.quantity == 0:
            self._delete_product_item(product_item)
            return None
        product_item = get_serializer_data(
            get_serializer_by_objects(serializer_class=ItemSerializer, objects=product_item)
        )
        return product_item

    def _get_product_item(self, product_slug: str) -> Item:
        """
        @param: Product model instance slug.
        @return: Item model instance.
        @raise: If Item model instance doesn't exist.
        """
        product_item = get_product_item(request=self.request, product_slug=product_slug)
        if product_item is None:
            raise exception_raiser(
                exception_class=exceptions.NotFound,
                msg=f"No such product with slug {product_slug}."
            )
        return product_item

    def _reduce_quantity_of_product_item(self, product_item: Item, product_item_quantity: int) -> Item:
        """
        Reduce quantity of Item model instance by request_data_serializer its parameter product_qty.
        @param product_item: Item model instance.
        @param product_item_quantity: Quantity of product on which need to reduce by default 1.
        @return: Item model instance.
        """
        product_item.quantity -= product_item_quantity
        product_item.save()
        return product_item

    def _delete_product_item(self, product_item: Item):
        """
        @param product_item: Item model instance.
        @return: None
        """
        product_item.delete()


class RemoveProductItemFromCart(ReduceQuantityOfProductItem):
    """Remove product item from customer cart."""
    def execute(self, product_slug: str) -> None:
        """
        Performer method.
        @return: None.
        """
        product_item = self._get_product_item(product_slug=product_slug)
        self._delete_product_item(product_item)