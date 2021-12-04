from django.contrib import admin
from .models import User,Airport,Flight,FlightPayment,Book,Alert

admin.site.register(User)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(FlightPayment)
admin.site.register(Book)
admin.site.register(Alert)
