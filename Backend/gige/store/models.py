# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from accounts.models import Profile

# # Create your models here.

# class Item(models.Model):
    
#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=500)
#     item_pic = models.ImageField(upload_to ='item_pic')
#     owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
#     price = models.IntegerField()
#     digital = models.BooleanField()
#     sold = models.BooleanField()
#     #category

#     def __str__(self):
#         return self.name


# class Transaction(models.Model):

#     item = models.OneToOneField(Item, on_delete=models.SET_NULL, blank=True, null=True)
#     customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
#     date_ordered = models.DateTimeField(auto_add_now=True)
#     transaction_id = models.CharField(max_length=200)

#     def __str__(self):
#         return self.transaction_id