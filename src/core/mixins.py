class SerializerByActionMixin:
    """Use different serializers for different actions in ViewSets."""
    default_serializer_class = None
    serializer_classes = {}  # {'action name': Any Serializer}

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)