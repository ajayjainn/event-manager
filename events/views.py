from django.shortcuts import render,HttpResponse,redirect

from django.contrib import messages
from .models import Event
import random
import string
import datetime

def home(request):
    return render(request,'events/home.html')

def about(request):
    return HttpResponse("<h1>Event about</h1>")

def join_event(request):
    if request.method=="POST":
        if not request.user.is_authenticated:
            return redirect('/events')
        code = request.POST.get("code",None)
        user = request.user
        event = Event.objects.get(code=code)
        if event:
            event.user.add(user)
            event.save()
            messages.success(request,"Joined successfully.")
            return redirect("event-home")
        else:
            messages.error("Enter valid code please")
            return redirect("event-join")
        
    else:
        code = request.GET.get('code','')
        return render(request,'events/acceptinvitationpage.html',{"code":code})   
        
def create_event(request):
    if request.method=="POST":
        name = request.POST.get("name")
        desc = request.POST.get("desc")
        date = datetime.datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
        organizer = request.user
        unique=False
        while (not unique):
            try: 
                code = ''.join(random.choices(string.ascii_lowercase, k=5))
                Event.objects.get(code=code)
            except Event.DoesNotExist: 
                unique=True
        ev = Event(organizer=organizer,name=name,desc=desc,date=date,code=code)
        ev.save()
        messages.success(request,f"Event created successfully.\n SHare the link with your friends: http://localhost:8000/events/join-event/?code={code}")
        return redirect('event-home')
    else:
        return render(request,'events/createevent.html')



        


        
        




        



