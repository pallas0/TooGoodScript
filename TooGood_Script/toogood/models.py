from django.db import models
from django.contrib.auth.models import User

class FavoriteRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.CharField(max_length=100)
    restaurant_name = models.CharField(max_length=200)
    has_bags_available = models.BooleanField(default=False)

    def __str__(self):
        return self.retaurant_name
