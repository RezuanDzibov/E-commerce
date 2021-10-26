from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.cart'

    def ready(self):
        import src.cart.signals
