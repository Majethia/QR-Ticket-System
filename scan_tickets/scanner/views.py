from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Tickets
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method == 'POST':
        data = request.POST['result']
        if data.startswith("TedXDypit"):
            Id = data.split('-')[-2]
            t = Tickets.objects.get(Id=Id)
            if t.Attended == 'Y':
                messages.error(request, f'{t.Name}, This Ticket has alredy been used')
            else:
                messages.info(request, f'{t.Name}, Verified you can enter')
                t.Attended = 'Y'
                t.save()
        else:
            messages.error(request, 'Thats not a valid ticket.')
        return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'index.html')
    
    
def import_data(request):
    records = Tickets.objects.all()
    records.delete()
    with open('export.csv', 'r') as f:
        data = f.read()
    data = data.split('\n')
    for i in data:
        i = [e.strip() for e in i.split(',')]
        Tickets.objects.create(Id = i[0], Name = i[1], Number = i[2], Email = i[3], Attended = 'N')
    return HttpResponse("Data Added")