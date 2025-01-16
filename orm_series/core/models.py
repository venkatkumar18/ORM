from django.db import models
from django.contrib.auth.models import User

# Restaurant
# Rating
# Sales

RESTAURANT_TYPE_CHOICE = [
    ("IN", "Indian"),
    ("CH", "Chinese"),
    ("FF", "Fast Food"),
    ("GR", "Greek"),
    ("IT", "Italian"),
    ("MX", "Mexican"),
    ("OT", "Other")
]

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(default="")
    date_opened = models.DateField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    restaurant_type = models.CharField(max_length=2, choices=RESTAURANT_TYPE_CHOICE)
    
    def __str__(self):
        return f"Restaurant: {self.name}"

class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f"Rating: {self.rating}"

class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    income = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField()
    