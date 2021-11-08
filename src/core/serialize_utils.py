from typing import Type

from rest_framework.serializers import Serializer


def serialize_objects(serializer_class: Type[Serializer], objects, many_objects: bool = False) -> Type[Serializer]:
    """
    The function serializes objects/object by passed serializer and return serialized object.
    many_objects - flag for saying that more than one object is passed.
    """

    serializer = serializer_class(objects, many=many_objects)
    return serializer


def serialize_data(serializer_class: Type[Serializer], data, many_objects: bool = False) -> Type[Serializer]:
    """
    The function serializes data by passed serializer and returns serialized object.
    many_objects - flag for saying that more than one object is passed.
    """
    serializer = serializer_class(data=data, many=many_objects)
    return serializer


def validate_serializer(serializer: Type[Serializer], raise_exception: bool = True) -> Type[Serializer]:
    """
    The function validates passed serializer object and returns serializer object.
    raise_exception - flag for saying that need to raise exception.
    """
    if serializer.is_valid(raise_exception=raise_exception):
        return serializer
