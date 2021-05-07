from django.contrib import admin
from .models import Item, Transaction, Todoitem

# Register your models here.

admin.site.register(Item)
admin.site.register(Transaction)
admin.site.register(Todoitem)