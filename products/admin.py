from django.contrib import admin
from .models import Laptop, ProductImages

# Tạo Inline cho ProductImages để hiển thị hình ảnh phụ trong trang Laptop
class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 3 # Số lượng form trống để thêm hình ảnh mới

# Tùy chỉnh hiển thị model Laptop
class LaptopAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')  # Hiển thị các cột trong danh sách
    inlines = [ProductImagesInline]  # Đưa ProductImages vào trang chi tiết laptop

# Đăng ký các model với admin
admin.site.register(Laptop, LaptopAdmin)
admin.site.register(ProductImages)
