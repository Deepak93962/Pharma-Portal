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
    payment_status = models.CharField(
    max_length=20,
    default="Pending",
    choices=[("Pending", "Pending"), ("Paid", "Paid")]
    )


    def __str__(self):
        return f"Order #{self.id} by {self.chemist.username} - {self.medicine.name}"


class CartOrder(models.Model):
    chemist = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, default="Pending")
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CartOrder #{self.id} - {self.chemist.username}"


class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, related_name="items")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price
    
class CartItem(models.Model):
    chemist = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chemist.username} - {self.medicine.name}"

    def get_total(self):
        return self.quantity * self.medicine.price
    

class Payment(models.Model):
    chemist = models.ForeignKey(User, on_delete=models.CASCADE)

    single_order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True
    )

    cart_order = models.ForeignKey(
        CartOrder, on_delete=models.CASCADE, null=True, blank=True
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.single_order:
            return f"SingleOrder {self.single_order.id} Payment"
        else:
            return f"CartOrder {self.cart_order.id} Payment"

