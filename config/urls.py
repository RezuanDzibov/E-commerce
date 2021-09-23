from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .yasg import urlpatterns as doc_urls
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/v1/cart/', include('cart.urls')),
    path('api/v1/product/', include('product.urls')),
    path('api/v1/order/', include('order.urls')),
    path('api/v1/customer/', include('customer.urls')),
    path('__debug__/', include(debug_toolbar.urls)),



]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)