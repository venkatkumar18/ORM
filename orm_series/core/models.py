from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
# Restaurant
# Rating
# Sales

def custom_validator(value):
    if not value.lower().startswith('a'):
        raise ValidationError("Field Value Must Begin With A/a")

class Restaurant(models.Model):
    
    class TypeChoices(models.TextChoices):
        INDIAN = "IN", "Indian"
        CHINESE = "CH", "Chinese"
        FASTFOOD = "FF", "FastFood"
        GREEK = "GR", "Greek"
        ITALIAN = "IT", "Italian"
        MEXICAN = "MX", "Mexican"
        OTHER = "OT", "Other"
        
    name = models.CharField(max_length=100,validators=[custom_validator])
    website = models.URLField(default="")
    date_opened = models.DateField()
    longitude = models.FloatField(validators=[MinValueValidator(-180),MaxValueValidator(180)])
    latitude = models.FloatField(validators=[MinValueValidator(-90),MaxValueValidator(90)])
    restaurant_type = models.CharField(max_length=2, choices=TypeChoices.choices)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True)
    
    class Meta():
        ordering = [Lower("name")]
        get_latest_by = "date_opened"
    
    def __str__(self):
        return f"Restaurant: {self.name}"

    def save(self,*args,**kwargs):
        print(f'MODEL CREATED - {self._state.adding}')
        super().save(*args,**kwargs)

class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    
    def __str__(self):
        return f"Rating: {self.rating}"

class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name='sale')
    income = models.DecimalField(max_digits=8, decimal_places=2)
    expenditure = models.DecimalField(max_digits=8,decimal_places=2)
    datetime = models.DateTimeField()
    
    
class Staff(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ManyToManyField(Restaurant, through='StaffRestaurant')
    
    def __str__(self):
        return self.name
    
class StaffRestaurant(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    salary = models.FloatField()