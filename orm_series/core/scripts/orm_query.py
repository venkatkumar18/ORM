from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection
from pprint import pprint
from django.contrib.auth.models import User
from django.db.models.functions import Lower

def run():
    # rating = Rating.objects.filter(restaurant__name__startswith='C')
    sale = Sale.objects.filter(restaurant__restaurant_type="CH")
    
    print(sale)
    
    
    
    pprint(connection.queries)
    