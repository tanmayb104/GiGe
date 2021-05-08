from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Item, Todoitem

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
    todolist = Todoitem.objects.filter(user=request.user.id)
    data = {"user": user, "items": items, "todolist": todolist}
    return render(request, 'give.html', data)

def itemView(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    user = User.objects.get(username=request.user.username)
    item =  Item.objects.get(id=pk)
    data = {"user": user, "item": item}
    return render(request, 'itemView.html', data)

def categoryView(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    user = User.objects.get(username=request.user.username)
    item =  Item.objects.filter(category=pk).exclude(owner=request.user.id)
    data = {"user": user, "items": item}
    return render(request, 'categoryView.html', data)

def itemAdd(request):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if (request.method == 'POST'):
        print("reached")
        name = request.POST['pname']
        description = request.POST['pdes']
        item_pic = request.POST['item_pic']
        owner = request.user.id
        price = request.POST['pcost']
        digital = request.POST['pdig']
        category = request.POST['pcat']

        item,created = Item.objects.get_or_create(name=name, description=description, item_pic=item_pic, owner=owner, price=price, digital=digital, status=False, category=category)
        if(created):
            messages.info(request, 'Item listed successfully')
            return redirect('give')
        else:
            messages.info(request, 'Item already exists')
            return redirect('give')

    else:
        user = User.objects.get(username=request.user.username)
        data = {"user": user}
        return render(request, 'itemAdd.html', data)


def giveItem(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    try:
        user = User.objects.get(username=request.user.username)
        item =  Item.objects.get(id=pk)
        data = {"user": user, "items": item}
        return render(request, 'giveItem.html', data)
    except:
        messages.info(request, 'Item does not exist')
        return render(request, 'give.html')


def itemDelete(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')
    
    try:
        item = Item.objects.get(user=request.user.id, id=pk)
        item.delete()
        messages.info(request, 'Item deleted successfully')
        return redirect('give')
    except:
        messages.info(request, 'Item does not exist')
        return redirect('give')


def itemEdit(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')
    
    if (request.method == 'POST'):
        
        try:
            item = Item.objects.get(user=request.user.id, id=pk)
            item.name = request.POST['name']
            item.description = request.POST['description']
            item.item_pic = request.POST['item_pic']
            item.price = request.POST['price']
            item.digital = request.POST['digital']
            item.category = request.POST['category']
            item.save()
            messages.info(request, 'Item edited successfully')
            return redirect('giveItem',pk=pk)
        except:
            messages.info(request, 'Item does not exist')
            return redirect('give')
    
    else:

        return render(request, 'edit.html')



def itemBuy(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    user = User.objects.get(username=request.user.username)
    trans = Transaction.object.create(item=pk,customer=request.user.id)
    trans.save()
    return render(request,'get.html')


def itemTodoadd(request):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if (request.method == 'POST'):
        heading = request.POST['heading']
        user = request.user.id

        item,created = Todoitem.objects.get_or_create(heading=heading, user=user)
        if(created):
            messages.info(request, 'Task created successfully')
            return redirect('give')
        else:
            messages.info(request, 'Item already exists')
            return redirect('give')

    else:
        return render(request,'give.html')


def itemTododelete(request,pk):

    if not request.user.is_authenticated:
        return render(request, 'login.html')

    try:
        task = Todoitem.objects.get(id=pk)
        task.delete()
        messages.info(request, 'Task completed')
        return redirect('give')
    except:
        messages.info(request, 'Task does not exist')
        return redirect('give')

