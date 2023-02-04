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
        try:
            event = Event.objects.get(code=code)
        except:
            event=None
        if code and not event:
            messages.error(request,"Enter valid invite code")
            return redirect("event-join")
        print(event)
        return render(request,'events/acceptinvitationpage.html',{"event":event})   
        
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

def manage_event(request):
    user=request.user 
    if not request.user.is_authenticated:
        return redirect('users-login')
    events = Event.objects.filter(organizer=user.id,date__gte=datetime.date.today())
    context={"events":events}
    return render(request,'events/manageevent.html',context=context)

def my_invitations(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('users-login')
    invitation = user.invitations.filter(date__gte=datetime.date.today())
    return render(request,'events/invitations.html',context={"invitations":invitation})



    



        


        
        




        



