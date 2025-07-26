from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('men', 'Men'),
    ('women', 'Women'),
    ('boys', 'Boys'),
    ('girls', 'Girls'),
    ('baby', 'Baby'),
]

SIZE_CHOICES = [
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
]

class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # <-- Add default here
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, default='M')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ProductSizeStock(models.Model):
    product = models.ForeignKey(Product, related_name="size_stock", on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.product.name} - {self.size}: {self.stock} in stock"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Admin approves reviews

    def __str__(self):
        return f"Review {self.rating} by {self.user} on {self.product.name}"
