from django.contrib import admin
from .models import Laptop, ProductImages

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1

@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]

admin.site.register(ProductImages)
