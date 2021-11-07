from typing import Type

from rest_framework.serializers import Serializer


def serialize_objects(serializer_class: Type[Serializer], objects, many_objects: bool = False) -> Type[Serializer]:
    serializer = serializer_class(objects, many=many_objects)
    return serializer


def serialize_data(serializer_class: Type[Serializer], data, many_objects: bool = False) -> Type[Serializer]:
    serializer = serializer_class(data=data, many=many_objects)
    return serializer


def validate_serializer(serializer: Type[Serializer]) -> Type[Serializer]:
    if serializer.is_valid(raise_exception=True):
        return serializer
