from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile
import uuid

# Create your models here.

class Item(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    item_pic = models.ImageField(upload_to ='item_pic')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    digital = models.BooleanField()
    status = models.BooleanField(default=False)

    categories=[
        ("General", "General"),
        ("Electronic", "Electronic"),
        ("Books", "Books"),
    ]
    category = models.CharField(max_length=15,choices=categories)

    def __str__(self):
        return self.name


class Transaction(models.Model):

    item = models.OneToOneField(Item, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="getter")
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.transaction_id


class Todoitem(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    heading = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.heading}-{self.user}"