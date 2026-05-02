from django.contrib import admin
from .models import Category, MenuItem, Customer, Staff, Order, OrderItem, DutySchedule

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DutySchedule)
