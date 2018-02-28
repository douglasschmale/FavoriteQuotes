from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Users, Items
from datetime import datetime
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = Users.objects.regvalidator(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
            print error
        return redirect('../')
    else:
        new_user = Users.objects.create(
        first = request.POST['first'],
        last = request.POST['last'],
        email = request.POST['email'].lower(),
        password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()),
        birthday = request.POST['birthday'],
        )
        request.session['user']=Users.objects.get(email=request.POST['email']).first
        request.session['id']=Users.objects.get(email=request.POST['email']).id
        return redirect('/dashboard')#+str(request.session['id']))

def login(request):
    error =  Users.objects.loginvalidator(request.POST)

    if len(error):
        for i in error:
            messages.error(request, i)
            print error
        return redirect('../')
    else:
        request.session['user']=Users.objects.get(email=request.POST['email']).first
        request.session['id']=Users.objects.get(email=request.POST['email']).id
        return redirect('/dashboard')

def wish_items(request, itemid):
    data = {
        'products': Items.objects.all().get(creator_id=request.session['id'])
    }
    return render(request, "wish_item/"+itemid, data)

def create(request):
    return render(request, "create.html")

def add(request):
    error = Items.objects.validator(request.POST)
    if len(error):
        for i in error:
            messages.error(request, i)
            print error
        return redirect('/create')
    new_item = Items.objects.create(
    product = request.POST['product'],
    creator_id = request.session['id'],
    )
    return redirect('/dashboard')

def dashboard(request):
    # print request.session['id']
    print Items.favorite
    data = {
        'favs': Items.objects.filter(favorite=request.session['id']).all(),
        'products': Items.objects.all().exclude(favorite=request.session['id'])
    }
    return render(request, "dashboard.html", data)

def favorited(request, itemid):
    favorited = Items.objects.get(id=itemid)
    current_user = Users.objects.get(id=request.session['id'])
    favorited.favorite.add(current_user)
    return redirect('/dashboard')

def remove(request, itemid):
    remove_me = Items.objects.get(id=itemid)
    current_user = Users.objects.get(id=request.session['id'])
    remove_me.favorite.remove(current_user)
    return redirect('/dashboard')


def delete(request, itemid):
    garbage = Items.objects.get(id=itemid)
    garbage.delete()
    return redirect('/dashboard')

def wish_items(request, itemid):
    data = {
        'product': Items.objects.get(id=itemid),
        'wishers': Users.objects.filter(user_favorite=itemid)
    }
    return render(request, "wish_items.html", data)

def logout(request):
    request.session.clear()
    return redirect('../')
