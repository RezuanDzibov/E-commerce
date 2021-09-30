from rest_framework import viewsets


viewsets,viewsets.ModelViewSet


class SerializerMixin:
    serializer_class = None

    def serialize(self, data):
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            return serializer
