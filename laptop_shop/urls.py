from django.contrib import admin
from django.urls import path
from products.views import laptop_list, laptop_detail, index, contact, about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),  # Home page
    path('contact', contact, name='contact'),  # Home page
    path('about', about, name='about'),  # Home page
    path('laptops/', laptop_list, name='laptop_list'),
    path('laptops/<int:pk>/', laptop_detail, name='laptop_detail'),  # URL for laptop detail
]
#fafdf
#thadsf
# Serve media files in development mode
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
