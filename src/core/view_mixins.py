from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedMixin:
    def get_permissions(self):
        self.permission_classes.append(IsAuthenticated)
        return [permission() for permission in self.permission_classes]


class SerializerByAction:
    default_serializer_class = None

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)