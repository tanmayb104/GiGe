from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Item

# Create your views here.

def get(request):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    user = User.objects.get(username=request.user.username)
    items =  Item.objects.exclude(owner=request.user.id).exclude(status=True)
    categories = ["General","Electronic","Books"]
    categoryItems = {}
    for i in categories:
        categoryItems[i] = items.filter(category=i).reverse()
        print(len(categoryItems[i]))
    data = {"user": user, "items": categoryItems}
    return render(request, 'get.html', data)

def give(request):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    user = User.objects.get(username=request.user.username)
    items =  Item.objects.filter(owner=request.user.id)
    data = {"user": user, "items": items}
    return render(request, 'give.html', data)

def itemView(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    user = User.objects.get(username=request.user.username)
    item =  Item.objects.get(id=pk)
    data = {"user": user, "items": item}
    return render(request, 'itemView.html', data)

def categoryView(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    user = User.objects.get(username=request.user.username)
    item =  Item.objects.filter(category=pk)
    data = {"user": user, "items": item}
    return render(request, 'categoryView.html', data)

def itemAdd(request):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if (request.method == 'POST'):
        name = request.POST['name']
        description = request.POST['description']
        item_pic = request.POST['item_pic']
        owner = request.user.id
        price = request.POST['price']
        digital = request.POST['digital']
        category = request.POST['category']

        item,created = Item.objects.get_or_create(name=name, description=description, item_pic=item_pic, owner=owner, price=price, digital=digital, status=False, category=category)
        if(created):
            return render(request,'give.html')
        else:
            messages.info(request, 'Item already exists')
            return redirect('give')
        

    else:
        user = User.objects.get(username=request.user.username)
        data = {"user": user}
        return render(request, 'itemAdd.html', data)

def itemBuy(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    user = User.objects.get(username=request.user.username)
    trans = Transaction.object.create(item=pk,customer=request.user.id)
    trans.save()
    return render(request,'get.html')