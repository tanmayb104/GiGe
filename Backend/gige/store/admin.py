from django.contrib import admin
from .models import Item, Transaction

# Register your models here.

admin.site.register(Item)
admin.site.register(Transaction)