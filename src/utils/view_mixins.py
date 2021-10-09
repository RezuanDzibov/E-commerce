from rest_framework import validators
from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedMixin:
    def get_permissions(self):
        self.permission_classes.append(IsAuthenticated)
        return [permission() for permission in self.permission_classes]


class SerializerByAction:
    serializer_classes = None

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)