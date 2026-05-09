from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):
    FOOD_TYPES = [
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    food_type = models.CharField(max_length=10, choices=FOOD_TYPES, default='Veg')
    price = models.FloatField()
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Menu)
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"