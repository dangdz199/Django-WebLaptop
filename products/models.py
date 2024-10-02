from django.db import models
from django.conf import settings

# Mô hình laptop
class Laptop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='laptops/')  # Hình ảnh chính của laptop
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Mô hình nhiều hình ảnh cho laptop
class ProductImages(models.Model):
    laptop = models.ForeignKey(Laptop, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='laptops/images/')  # Thêm nhiều ảnh cho laptop
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.laptop.name}"

# Mô hình đơn hàng
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id}"

    @property
    def get_total_price(self):
        # Tính tổng giá trị tất cả các sản phẩm trong đơn hàng
        total = sum([item.get_total_price for item in self.items.all()])
        # Áp dụng thuế từ cấu hình settings
        total_with_tax = total * (1 + settings.TAX_RATE)
        return total_with_tax

    def apply_discount(self):
        # Tính tổng giá trị sau thuế
        total = self.get_total_price
        # Nếu tổng giá trị vượt qua ngưỡng giảm giá, áp dụng giảm giá
        if total > settings.DISCOUNT_THRESHOLD:
            total_with_discount = total * (1 - settings.DISCOUNT_RATE)
            return total_with_discount
        return total

# Mô hình mục sản phẩm trong đơn hàng
class OrderItem(models.Model):
    product = models.ForeignKey(Laptop, on_delete=models.CASCADE)  # Sử dụng Laptop làm sản phẩm
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def get_total_price(self):
        # Tính tổng giá trị của sản phẩm này
        return self.quantity * self.product.price
