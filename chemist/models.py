from django.db import models
from vendor.models import Medicine   # ✅ import from vendor, not local
from django.contrib.auth.models import User
# Create your models here.
class ChemistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.shop_name
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    chemist = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    is_stock_updated = models.BooleanField(default=False) 

    def __str__(self):
        return f"Order #{self.id} by {self.chemist.username} - {self.medicine.name}"