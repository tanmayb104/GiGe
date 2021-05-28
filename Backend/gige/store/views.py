from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Item, Todoitem, Transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

@login_required
def get(request):

    user = User.objects.get(username=request.user.username)
    items =  Item.objects.exclude(owner=request.user.id).exclude(status=True)
    categories = ["General","Electronic","Books"]
    categoryItems = {}
    for i in categories:
        categoryItems[i] = items.filter(category=i).reverse()[:3]
    data = {"user": user, "items": categoryItems}
    return render(request, 'get.html', data)


@login_required
def give(request):

    user = User.objects.get(username=request.user.username)
    items =  Item.objects.filter(owner=request.user.id)
    todolist = Todoitem.objects.filter(user=request.user.id)
    data = {"user": user, "items": items, "todolist": todolist}
    return render(request, 'give.html', data)


@login_required
def itemView(request,pk):

    user = User.objects.get(username=request.user.username)
    item =  Item.objects.get(id=pk)
    data = {"user": user, "item": item}
    return render(request, 'itemView.html', data)


@login_required
def categoryView(request,pk):

    user = User.objects.get(username=request.user.username)
    item =  Item.objects.filter(category=pk).exclude(owner=request.user.id)
    data = {"user": user, "items": item, "category":pk}
    return render(request, 'categoryView.html', data)


@login_required
def itemAdd(request):

    if (request.method == 'POST'):
        name = request.POST['pname']
        description = request.POST['pdes']
        item_pic = request.POST['pimg']
        item_pic = item_pic.replace(" ","_")
        item_pic = item_pic.replace("(","")
        item_pic = item_pic.replace(")","")
        item_pic = "item_pic/"+ item_pic
        price = request.POST['pcost']
        digital = request.POST['pdig']
        category = request.POST['pcat']
        days = request.POST['pday']
        item,created = Item.objects.get_or_create(name=name, description=description, item_pic=item_pic, owner=request.user, price=price, digital=digital, status=False, category=category, days=days)
        if(created):
            messages.success(request, 'Item listed successfully')
            return redirect('give')
        else:
            messages.error(request, 'Item already exists')
            return redirect('give')

    else:
        user = User.objects.get(username=request.user.username)
        data = {"user": user}
        return render(request, 'itemAdd.html', data)


# @login_required
# def giveItem(request,pk):

#     try:
#         user = User.objects.get(username=request.user.username)
#         item =  Item.objects.get(id=pk)
#         data = {"user": user, "items": item}
#         return render(request, 'giveItem.html', data)
#     except:
#         messages.error(request, 'Item does not exist')
#         return render(request, 'give.html')


@login_required
def itemDelete(request,pk):
    
    try:
        item = Item.objects.get(id=pk)
        item.delete()
        messages.success(request, 'Item deleted successfully')
        return redirect('give')
    except:
        messages.error(request, 'Item does not exist')
        return redirect('give')


@login_required
def itemEdit(request,pk):
    
    if (request.method == 'POST'):
        
        item = Item.objects.get(id=pk)
        item.name = request.POST['name']
        item.description = request.POST['description']
        if(request.POST['p-img']):
            item_pic = request.POST['p-img']
            item_pic = item_pic.replace(" ","_")
            item_pic = item_pic.replace("(","")
            item_pic = item_pic.replace(")","")
            item_pic = "item_pic/"+ item_pic
            item.item_pic = item_pic
        item.price = request.POST['price']
        # item.category = request.POST['category']
        item.days = request.POST['days']
        item.save()
        messages.success(request, 'Item edited successfully')
        return redirect('itemEdit',pk=pk)
    
    else:
        try:
            user = User.objects.get(username=request.user.username)
            item =  Item.objects.get(id=pk)
            data = {"user": user, "item": item}
            return render(request, 'edit.html', data)
        except:
            messages.error(request, 'Item does not exist')
            return redirect('give')
        


@login_required
def itemBuy(request,pk):

    user = User.objects.get(username=request.user.username)
    item = Item.objects.get(id=pk)
    trans,created = Transaction.objects.get_or_create(item=item,customer=request.user)
    if(created):
        messages.success(request, 'Order placed successfully')
        return redirect('getOrders')
    else:
        messages.error(request, 'Order already placed')
        return redirect('getOrders')


@login_required
def Todoadd(request):

    if (request.method == 'POST'):
        heading = request.POST['new-task']
        user = request.user

        item,created = Todoitem.objects.get_or_create(heading=heading, user=user)
        if(created):
            messages.success(request, 'Task created successfully')
            return redirect('give')
        else:
            messages.error(request, 'Item already exists')
            return redirect('give')

    else:
        return render(request,'get.html')


@login_required
def Tododelete(request,pk):

    try:
        task = Todoitem.objects.get(id=pk)
        task.delete()
        messages.success(request, 'Task completed')
        return redirect('give')
    except:
        messages.error(request, 'Task does not exist')
        return redirect('give')


@login_required
def itemSearch(request):

    pk = request.GET['search']
    items = Item.objects.filter(Q(name__icontains=pk)|Q(description__icontains=pk)).distinct().exclude(owner=request.user.id)
    user = User.objects.get(username=request.user.username)
    data = {"user": user, "items": items}
    return render(request, 'searchItem.html', data) 


@login_required
def getOrders(request):

    user = User.objects.get(username=request.user.username)
    orders = Transaction.objects.filter(customer=user)
    data = {"user": user, "orders": orders}
    return render(request,'orders_getter.html',data)


@login_required
def giveOrders(request):

    user = User.objects.get(username=request.user.username)
    orders = Transaction.objects.filter(item__owner=user)
    data = {"user": user, "orders": orders}
    return render(request,'orders_giver.html',data)


@login_required
def DeleteOrders(request,pk):

    try:
        transaction = Transaction.objects.get(transaction_id=pk)
        transaction.delete()
        messages.success(request, 'Order deleted')
        return redirect('getOrders')
    except:
        messages.error(request, 'Order does not exists')
        return redirect('getOrders')