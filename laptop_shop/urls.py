from django.contrib import admin
from django.urls import path
from products.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),  # Home page
    path('contact', contact, name='contact'),  # Home page
    path('about', about, name='about'),  # Home page
    path('laptops/', laptop_list, name='laptop_list'),
    path('laptops/<int:pk>/', laptop_detail, name='laptop_detail'),  # URL for laptop detail
    path('add-to-cart/<int:laptop_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
