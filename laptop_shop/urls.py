from django.contrib import admin
from django.urls import path
from products.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),  # Home page
    path('contact', contact, name='contact'),  # Home page
    path('about', about, name='about'),  # Home page
    path('laptops/', laptop_list, name='laptop_list'),
    path('laptops/<int:pk>/', laptop_detail, name='laptop_detail'),  # URL for laptop detail
    path('cart/', view_cart, name='cart'),
    path('add_to_cart/<int:laptop_id>/', add_to_cart, name='add_to_cart'),
    path('update_cart/<int:laptop_id>/', update_cart, name='update_cart'),
    path('remove_from_cart/<int:laptop_id>/', remove_from_cart, name='remove_from_cart'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)