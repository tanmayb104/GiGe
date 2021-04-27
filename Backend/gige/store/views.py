from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Item

# Create your views here.

def get(request):
    user = User.objects.get(username=request.user.username)
    items =  Item.objects.exclude(owner=request.user.id, status=True)
    categories = ["General","Electronic","Books"]
    categoryItems = {}
    for i in categories:
        categoryItems[i] = items.filter(category=i)
    data = {"user": user[0], "items": items}
    return render(request, 'get.html', data)

def give(request):
    user = User.objects.get(username=request.user.username)
    items =  Item.objects.filter(owner=request.user.id)
    data = {"user": user[0], "items": items}
    return render(request, 'give.html', data)

def itemView(request,pk):
    user = User.objects.get(username=request.user.username)
    item =  Item.objects.get(id=pk)
    data = {"user": user[0], "items": item}
    return render(request, 'itemView.html', data)

def categoryView(request,pk):
    user = User.objects.get(username=request.user.username)
    item =  Item.objects.filter(category=pk)
    data = {"user": user[0], "items": item}
    return render(request, 'categoryView.html', data)

def itemAdd(request):

    if (request.method == 'POST'):
        name = request.POST['name']
        description = request.POST['description']
        item_pic = request.POST['item_pic']
        owner = request.user.id
        price = request.POST['price']
        digital = request.POST['digital']
        category = request.POST["category"]

        item,created = Item.objects.get_or_create(name=name, description=description, item_pic=item_pic, owner=owner, price=price, digital=digital, status=False, category=category)
        if(created):
            return render(request,'give.html')
        else:
            messages.info(request, 'Item already exists')
            return redirect('give')
        

    else:
        user = User.objects.get(username=request.user.username)
        data = {"user": user[0]}
        return render(request, 'itemAdd.html', data)