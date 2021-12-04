from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Airport,Flight,Book,FlightPayment,Alert
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.core.mail import send_mail
import math,random
from itertools import chain
from django.contrib.auth.decorators import login_required
import datetime




def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(6) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP




def index(request):
    now = datetime.datetime.now()
    flights = Flight.objects.filter(departure_date=now).delete()
    if request.user.is_authenticated:
        a = Alert.objects.filter(user=request.user).all()
        for i in a:
            flight = Flight.objects.filter(cityfrom=i.alertcityfrom,cityto=i.alertcityto).first()
            if flight:
                if flight.price < 500:
                    html_content = f'<table><tr><th>Name</th><td>{request.user.username}</td></tr><tr><th>CityFrom</th><td>{flight.cityfrom.city}</td></tr><tr><th>Cityto</th><td>{flight.cityto.city}</td></tr><tr><th>Lowestprice</th><td>{flight.price}</td></tr></table>'
                    send_mail('Lowest price alert',"hello",'htetaung200071@gmail.com',[request.user.email], fail_silently=False,html_message=html_content)
                    i.delete()
    return render(request,"travel/flights.html",{
        "airports":Airport.objects.all(),
        "newyork":Airport.objects.filter(code="JFK").first(),
        "london":Airport.objects.filter(code="LHR").first(),
        "paris":Airport.objects.filter(code="CDG").first()
    })



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"] 
        password = request.POST["password"] 
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("home"))          
        else:
            return render(request,"travel/login.html",{
                "message":"invalid account"
            })          
    return render(request,"travel/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"] 
        email = request.POST["email"] 
        password = request.POST["password"] 
        cpassword = request.POST["cpassword"] 
        if password != cpassword:
            return render(request,"travel/register.html",{
                "message":"password didn't match"
            })
        else:
            try: 
                n = generateOTP()
                send_mail('OTP request key',n,'htetaung200071@gmail.com',[email], fail_silently=False)             
                user = User.objects.create_user(username=username,email=email,password=password,otp=n)
                login(request,user)
                return HttpResponseRedirect(reverse("otp")) 
            except IntegrityError:
                return render(request,"travel/register.html",{
                        "message":"username is already exists "
                    })
    return render(request,"travel/register.html")

@login_required(login_url='login')
def otp(request):   
    if request.method == "POST":   
        otp = request.POST["otp"]
        if User.objects.filter(otp=otp).first():
            return HttpResponseRedirect(reverse("home"))
        else:
            user = User.objects.filter(username=request.user.username).first()
            user.delete()
            return render(request,"travel/register.html",{
                "message":"otp number is wrong"
            })
    return render(request,"travel/otp.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))   


def search(request):
    if request.method == "POST":
        departuredate = request.POST.get("departuredate")
        cityfrom = request.POST.get("cityfrom")
        cityto = request.POST.get("cityto")
        round = request.POST.get("tripType")
        if round == "round":
            flights = list(chain( Flight.objects.filter(cityfrom=cityfrom,cityto=cityto).all(),Flight.objects.filter(cityfrom=cityto,cityto=cityfrom).all()))  
        elif departuredate and cityto and cityfrom:  
            flights = Flight.objects.filter(cityfrom=cityfrom,cityto=cityto,departure_date=departuredate).all()
        elif cityto and cityfrom:
            flights = Flight.objects.filter(cityfrom=cityfrom,cityto=cityto).all()
        elif cityfrom:
            flights = Flight.objects.filter(cityfrom=cityfrom).all()
        elif cityfrom and departuredate:
            flights = Flight.objects.filter(cityfrom=cityfrom,departure_date=departuredate).all()
        elif cityto and departuredate:
            flights = Flight.objects.filter(cityto=cityto,departure_date=departuredate).all()
        elif cityto:
            flights = Flight.objects.filter(cityto=cityto).all()
        elif departuredate:
            flights = Flight.objects.filter(departure_date=departuredate).all()
        else:
            return render(request,"travel/search.html",{
            "airports":Airport.objects.all()
        })
    return render(request,"travel/search.html",{
            "flights":flights,
            "airports":Airport.objects.all(),
           
        })


def detail(request,id):
    flight = Flight.objects.get(id=id) 
    if request.user.is_authenticated:
        if request.method == "POST":
            b = Book.objects.filter(user=request.user,flight=flight).first()
            if b:
                b.delete()
            passengers = request.POST["passengers"]
            totalprice = request.POST["totalprice"]
            book = Book.objects.create(user=request.user,flight=flight,passengers=passengers,price=totalprice)
            book.save()
            print(book.price)
            return HttpResponseRedirect(reverse('payment',args=(flight.id,)))      
    else:
        return HttpResponseRedirect(reverse('login')) 
    return render(request,"travel/detail.html",{
        "flight":flight,
        "airports":Airport.objects.all(),

    })

@login_required(login_url='login')
def payment(request,id):
    flight = Flight.objects.get(id=id)
    if request.method == "POST":
        cardname = request.POST["cardname"]
        cardtype = request.POST["cardtype"]
        cardholder = request.POST["cardholder"]
        cardnumber = request.POST["cardnumber"]
        carddate = request.POST["carddate"]
        cardcode = request.POST["cardcode"]
        p = FlightPayment.objects.create(name=cardname,type=cardtype,holder=cardholder,number=cardnumber,date=carddate,code=cardcode)
        p.save()
        b = Book.objects.filter(user=request.user,flight=flight).first()
        b.payment = p
        b.save()
        print(b.price)
        html_content = f'<table><tr><th>Name</th><td>{request.user.username}</td></tr><tr><th>Flight name</th><td>{b.flight.name}</td></tr><tr><th>Passengers</th><td>{b.passengers}</td></tr><tr><th>Total price</th><td>{b.price}</td></tr></table>'
        send_mail('Successfully Booking Flight','hello','htetaung200071@gmail.com',[request.user.email], fail_silently=False,html_message=html_content) 
        return HttpResponseRedirect(reverse('success'))
    return render(request,"travel/payment.html",{
        "flight":flight
    })


@login_required(login_url='login')
def success(request):
    return render(request,"travel/success.html")

  
def about(request):
    return render(request,"travel/about.html")


@login_required(login_url='login')
def account(request):
    return render(request,"travel/account.html",{
        "alerts":Alert.objects.filter(user=request.user).all(),
        "airports":Airport.objects.all(),
        "flights":Book.objects.filter(user=request.user).all()
    })


@login_required(login_url='login')
def delete(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(reverse('home'))

@login_required(login_url='login')
def alert(request):
    if request.method == "POST":
        cityfrom = request.POST["cityfrom"]
        cityto = request.POST["cityto"]
        cf = Airport.objects.get(id=cityfrom)
        ct = Airport.objects.get(id=cityto)
        a = Alert.objects.create(user=request.user,alertcityfrom=cf,alertcityto=ct)
        a.save()
        return HttpResponseRedirect(reverse('account'))


@login_required(login_url='login')
def alertdelete(request,id):
    a = Alert.objects.get(id=id)
    a.delete()
    return HttpResponseRedirect(reverse('account'))
