class SerializerByActionMixin:
    """ Simple mixin for use different mixins in ViewSets by action type """
    default_serializer_class = None

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)