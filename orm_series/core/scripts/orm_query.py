from core.models import Restaurant, Rating, Sale, Staff, StaffRestaurant
from django.utils import timezone
from django.db import connection
from pprint import pprint
from django.contrib.auth.models import User
from django.db.models.functions import Lower, Upper, Concat, Length, Coalesce
from django.db.models import CharField, Value, Avg, Min, Max, Sum, Count, F, Q, Case, When
import random, itertools

def run():
    
    dates = []
    first_date = Sale.objects.aggregate(Min=Min('datetime'))['Min']
    last_date = Sale.objects.aggregate(Max=Max('datetime'))['Max']
    
    count = itertools.count()
    while (dt := first_date + timezone.timedelta(days=10 * next(count)) ) <= last_date:
        dates.append(dt)
        
    whens = [
        When(datetime__range=(dt, dt + timezone.timedelta(days=10)), then=Value(dt.date()))
        for dt in dates
    ]
    
    cases = Case(
        *whens,
        output_field=CharField()
    )
    
    sales = Sale.objects.annotate(
        daterange=cases
    ).values('daterange').annotate(total_sales=Sum('income'))
        
    print(sales)
    
    pprint(connection.queries)
    