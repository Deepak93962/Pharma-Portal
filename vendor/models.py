from django.db import models

class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('Tablet', 'Tablet'),
        ('Syrup', 'Syrup'),
        ('Injection', 'Injection'),
        ('Ointment', 'Ointment'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)

    def __str__(self):
        return self.name
