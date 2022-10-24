from django.db import models

# Create your models here.
class Ticket(models.Model):
    T_id = models.IntegerField(primary_key=True)
    T_hash = models.CharField(max_length=255)

class Tickets(models.Model):
    Id = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=255)
    Number = models.CharField(max_length=255)
    Email = models.CharField(max_length=255, unique=True)
    Attended = models.CharField(max_length=255)