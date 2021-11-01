from rest_framework.serializers import Serializer


class SerializerMixin:
    serializer_class = None

    def serialize(self, data):
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            return serializer


def serialize_objects(serializer_class, objects, many_objects: bool = False) -> Serializer:
    serializer = serializer_class(objects, many=many_objects)
    return serializer


def serialize_data(serializer_class, data, many_objects: bool = False) -> Serializer:
    serializer = serializer_class(data=data, many=many_objects)
    return serializer


def validate_serializer(serializer) -> Serializer:
    if serializer.is_valid(raise_exception=True):
        return serializer
