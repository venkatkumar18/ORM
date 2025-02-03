from core.models import Restaurant, Rating, Sale, Staff, StaffRestaurant, Product, Order, Comment
from django.utils import timezone
from django.db import connection
from pprint import pprint
from django.contrib.auth.models import User
from django.db.models.functions import Lower, Upper, Concat, Length, Coalesce
from django.db.models import CharField, Value, Avg, Min, Max, Sum, Count, F, Q, Case, When, Subquery, OuterRef, Exists
import random, itertools
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

def run():

    restaurant = Restaurant.objects.first()
    comment = Comment.objects.filter(
        restaurant=restaurant
    )
    print(comment)

    pprint(connection.queries)
    