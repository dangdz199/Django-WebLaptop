from django.db import models

class Laptop(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='laptops/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
