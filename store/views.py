from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as U,auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import math, random
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from .models import *
from django.views.generic import ListView,DetailView
from django.http import JsonResponse
import json
# Create your views here.
def register(request):
    if request.method == "POST":
                
            username = request.POST.get('username')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            request.session['email']= email
        
            print(request.session.get("email"))
            if password == confirm_password:
                if User.objects.filter(email=email).exists():
                    messages.info(request,"email is already exists")
                    return redirect('register')
                    
                else:
                        user = User.objects.create_user(email)
                        user.set_password(password)
                        user.save()
                        return redirect('login')
            else:
                print("There is no post")
                return render(request,"store/register.html")

    return render(request,'store/register.html')
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email= request.POST.get('email')
        request.session['email']=email
        print(request.session.get('email'))
        print(username,password)
        User = authenticate(email=email,username=username, password=password)
        if User  is not None:
            auth.login(request, User)
            return redirect("home")
        else:
            messages.info(request,"Invalid username")
            return redirect("login")
    return render(request,'store/login.html')

def home(request):
        if request.method == "POST":
            email=request.session.get('email')
            print(email)
            logout(request)
        return render(request,"course/home.html")

def forgot_password(request):
    if request.method == "POST":
        print(request.POST)
        email = request.POST['email']
        # print(email)
        
        if User.objects.filter(email=email).exists():

                email= request.POST.get('email')
                request.session.get('email')
                return redirect('course:forget_password')
        else:
            messages.info(request,"email is already exists")
            return redirect('course:change_password')
    return render(request,'store/forgot_password.html')

User = get_user_model()

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     print(OTP)
     return OTP

def send_otp(request):
   
     email=request.POST.get("email")
     request.session['email']=email
     print(email)   
     o=generateOTP()
     htmlgen = '<p>Your OTP is <strong>o</strong></p>'
     send_mail(
      subject="Reset Forget password", 
      message= f'OTP request {o}',
      from_email=settings.EMAIL_HOST_USER,
      recipient_list=[email],
      )

     return HttpResponse(o)


def reset_password(request):
    if request.method=='POST':
        nw=request.POST.get('nw')
        print(nw)
        cw= request.POST.get('cw')
        print(cw)
        email = request.session.get("email")
        print("--------------------------",email)
        try: 
            u=User.objects.get(email=email)
            u.set_password(cw)
            u.save()
            print("password changed")
            return redirect("login")
        except ObjectDoesNotExist:
            return HttpResponse("not changed")
    else:
        return render(request,'store/reset_password.html')

def changed(request):
    return render(request,"course/changed.html")

def logoutfunction(request):
        logout(request)
        return redirect("course:login")
   
def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
        
		order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)
def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)