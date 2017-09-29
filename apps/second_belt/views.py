from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.contrib import messages
from models import*
import bcrypt
from datetime import datetime

def index(request):
  request.session['log'] = False
  return render(request,"second_belt/index.html")

def login(request):
  if request.method == 'POST':
    request.session['log_reg'] = 'log'
    error = User.objects.login_check(request.POST)
    if len(error):
      messages.error(request, error, extra_tags="login")
      return redirect('/')
    else:
      request.session['log'] = True
      request.session['user_id'] = User.objects.get(username = request.POST['username']).id
      return redirect('/dashboard')
  return redirect('/')

def register(request):
  if request.method == "POST":
    request.session['log_reg']='reg'
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
      for tag,error in errors.iteritems():
        messages.error(request,error,extra_tags=tag)
      return redirect('/')
    secure_password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
    hiredate = datetime.strptime(request.POST['date_hired'], "%Y-%m-%d")
    User.objects.create(name=request.POST['name'], username=request.POST['username'], password = secure_password, date_hire = hiredate)
    request.session['log'] = True
    request.session['user_id'] = User.objects.last().id
    return redirect('/dashboard')
  return redirect('/')

def dashboard(request):
  if request.session['log']:
    myself = User.objects.get(id = request.session['user_id'])
    mycreateditem = Item.objects.filter(creater = myself)
    otheritem = Item.objects.exclude(creater = myself).exclude(follower = myself)
    othercreater = User.objects.exclude(id = request.session['user_id'])
    myadditem = list(myself.followitems.all())
    context = {
      "myself": myself,
      "mycreateditems": mycreateditem,
      "otheritems": otheritem,
      "othercreaters": othercreater,
      "myadditems": myadditem
    }
    return render(request, "second_belt/dashboard.html", context)
  return redirect('/')

def showadd(request):
  if request.session['log']:
    return render(request, 'second_belt/addnew.html')
  return redirect('/')

def create(request):
  if request.session['log']:
    errors = Item.objects.item_check(request.POST)
    print errors
    if len(errors):
      for tag, error in errors.iteritems():
        messages.error(request,error,extra_tags=tag)
      return redirect('/wish_items/create')
    else:
      Item.objects.create(item_name = request.POST['item'], creater = User.objects.get(id = request.session['user_id']))
      return redirect('/dashboard')
  return redirect('/')

def addlist(request, otheritem_id):
  addeditem = Item.objects.get(id= otheritem_id)
  myself = User.objects.get(id=request.session['user_id'])
  myself.followitems.add(addeditem)
  return redirect('/dashboard')

def remove(request, myadditem_id):
  removeitem = Item.objects.get(id = myadditem_id)
  myself = User.objects.get(id=request.session['user_id'])
  myself.followitems.remove(removeitem)
  return redirect('/dashboard')

def delete(request, mycreateditem_id):
  deleteitem = Item.objects.get(id = mycreateditem_id)
  myself = User.objects.get(id=request.session['user_id'])
  myself.createitems.filter(id = mycreateditem_id).delete()
  return redirect('/dashboard')

def showitem(request, showitem_id):
  showeditem = Item.objects.get(id = showitem_id)
  useradd = list(showeditem.follower.all())
  context = {
    "showeditems": showeditem,
    "useradds": useradd
  }
  return render(request, "second_belt/showitem.html", context)

def logout(request):
  del request.session['user_id']
  return redirect('/')











