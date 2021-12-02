from collections import OrderedDict
from typing import Type

from rest_framework.serializers import Serializer


def get_serializer_by_objects(
    serializer_class: Type[Serializer],
    objects,
    many_objects: bool = False
) -> Type[Serializer]:
    """
    @param serializer_class: Any serializer class.
    @param objects: Any model instance or queryset of instances.
    @param many_objects: Serializer flag many. By, default False.
    @return: Any serializer class.
    """
    serializer = serializer_class(objects, many=many_objects)
    return serializer


def get_serializer_by_data(serializer_class: Type[Serializer], data, many_objects: bool = False) -> Type[Serializer]:
    """
    @param serializer_class: Any serializer class.
    @param data: Data for serializing.
    @param many_objects: Serializer flag many. By, default False.
    @return: Any serializer class.
    """
    serializer = serializer_class(data=data, many=many_objects)
    return serializer


def get_validated_serializer(serializer: Type[Serializer], raise_exception: bool = True) -> Type[Serializer]:
    """
    @param serializer: Any serializer class.
    @param raise_exception: The method flag is valid. By, default True.
    @return: Any serializer class.
    """
    if serializer.is_valid(raise_exception=raise_exception):
        return serializer


def get_serializer_data(serializer: Type[Serializer]) -> Type[OrderedDict]:
    """
    @param serializer: Any Serializer subclass.
    @return: Serializer data property.
    """
    return serializer.data
