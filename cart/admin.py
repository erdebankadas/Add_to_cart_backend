from django.contrib import admin

# Register your models here.
from .models import OrderItem, User, Cart, DeliveryCost

admin.site.register(User)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(DeliveryCost)