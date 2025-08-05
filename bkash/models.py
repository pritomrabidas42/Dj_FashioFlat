from django.db import models
from orders.models import Order

class BkashPayment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"bKash Payment for Order {self.order.id}"
