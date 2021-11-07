from rest_framework.routers import DefaultRouter

from . import views


app_name = "product"


router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("categories", views.CategoryViewSet)
router.register("images", views.ImageViewSet)


urlpatterns = router.urls
