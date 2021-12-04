from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    otp = models.CharField(max_length=10)



class Airport(models.Model):
    city = models.CharField(max_length=64)
    code = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.city}:{self.code}"



class Flight(models.Model):
    name = models.CharField(max_length=64)
    cityfrom = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="departure")
    cityto = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="arrival")
    departure_date = models.DateField()
    duration = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.cityfrom} to {self.cityto} {self.departure_date} {self.duration} {self.price}"



class FlightPayment(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    holder = models.CharField(max_length=64)
    number = models.IntegerField()
    code = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.name}"
    

class Book(models.Model):
    payment = models.ForeignKey(FlightPayment,on_delete=models.CASCADE,related_name="fp",null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="u")
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE,related_name="f")
    price = models.CharField(max_length=64)
    passengers = models.IntegerField()


class Alert(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="uu")
    alertcityfrom = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="alertf")
    alertcityto = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="alertt")
