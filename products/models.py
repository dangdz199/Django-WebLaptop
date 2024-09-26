from django.db import models

class Laptop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='laptops/')  # Hình ảnh chính của laptop
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImages(models.Model):
    laptop = models.ForeignKey(Laptop, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='laptops/images/')  # Thêm nhiều ảnh cho laptop
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.laptop.name}"
