from django.contrib import admin

# Register your models here.
from .models import Ticket, Tickets

admin.site.register((Ticket, Tickets))