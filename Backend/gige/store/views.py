from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Item, Todoitem
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
        categoryItems[i] = items.filter(category=i).reverse()
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
        owner = request.user.id
        price = request.POST['pcost']
        digital = request.POST['pdig']
        category = request.POST['pcat']

        item,created = Item.objects.get_or_create(name=name, description=description, item_pic=item_pic, owner=owner, price=price, digital=digital, status=False, category=category)
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
        item = Item.objects.get(user=request.user.id, id=pk)
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
        print(request.POST)
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.item_pic = request.POST['p-img']
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
    trans = Transaction.object.create(item=pk,customer=request.user.id)
    trans.save()
    return render(request,'get.html')


@login_required
def Todoadd(request):

    print("hi")
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
        messages.error(request, 'Task completed')
        return redirect('give')
    except:
        messages.error(request, 'Task does not exist')
        return redirect('give')


@login_required
def itemSearch(request,pk):

    items = Item.objects.filter(Q(name__icontains=pk)|Q(description__icontains=pk)).distinct()
    user = User.objects.get(username=request.user.username)
    data = {"user": user, "items": items}
    # return render(request, 'search.html', data)


