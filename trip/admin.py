from django.contrib import admin
from .models import (
    Vehicle,
    Vehicle_Make,
    Vehicle_Model,
    Driver,
    Customer,
    Consignee,
    Trip,
    Shipper,
    Service,
    Estimate,
    Invoice,
    Payment,
    Expense_Category,
    Expense,
    Reminder,
    Load
)

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Vehicle_Make)
admin.site.register(Vehicle_Model)
admin.site.register(Driver)
admin.site.register(Customer)
admin.site.register(Trip)
admin.site.register(Consignee)
admin.site.register(Shipper)
admin.site.register(Service)
admin.site.register(Estimate)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Expense_Category)
admin.site.register(Expense)
admin.site.register(Reminder)
admin.site.register(Load)