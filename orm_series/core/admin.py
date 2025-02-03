from django.contrib import admin
from core.models import Restaurant, Sale, Rating, Product, Order, Comment
# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'rating']


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Sale)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Comment)

