from django.shortcuts import render
from core.models import Restaurant,Sale,Rating, Staff, StaffRestaurant
from django.db.models import Sum, Prefetch
from django.utils import timezone

# Create your views here.
def index(request):

    jobs = StaffRestaurant.objects.prefetch_related('staff','restaurant')
    for job in jobs:
       print(job.staff.name, end='  -   ')
       print(job.restaurant.name)
    

    return render(request, 'index.html')