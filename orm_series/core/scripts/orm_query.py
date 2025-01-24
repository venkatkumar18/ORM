from core.models import Restaurant, Rating, Sale, Staff, StaffRestaurant
from django.utils import timezone
from django.db import connection
from pprint import pprint
from django.contrib.auth.models import User
from django.db.models.functions import Lower, Upper, Concat, Length
from django.db.models import CharField, Value, Avg, Min, Max, Sum, Count
import random

def run():

    restaurant = Restaurant.objects.annotate(sum=Sum('sale__income')).values('sum')
    print(restaurant.aggregate(output=Avg('sum')))
    pprint(connection.queries)
    