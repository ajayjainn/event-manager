from django.shortcuts import render,HttpResponse,redirect

from django.contrib import messages
from .models import Event
import random
import string
import datetime
from django.conf import settings
from django.core.mail import send_mail
def home(request):
    return render(request,'events/home.html',context={"title":"Home"})

def about(request):
    return render(request,'events/about.html',context={"title":"Our team"})

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
        return render(request,'events/acceptinvitationpage.html',{"event":event,"title":"Join an event"})   
        
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
        return redirect('event-email-send')
    else:
        return render(request,'events/createevent.html',context={"title":"Create an event"})

def manage_event(request):
    user=request.user 
    if not request.user.is_authenticated:
        return redirect('login')
    events = Event.objects.filter(organizer=user.id,date__gte=datetime.date.today())
    context={"events":events,"title":"Manage Events"}
    return render(request,'events/management.html',context=context)

def my_invitations(request):
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    invitation = user.invitations.filter(date__gte=datetime.date.today())
    return render(request,'events/invitations.html',context={"invitations":invitation,"title":"My invitations"})

def send_email(request) :
        if request.method=="POST":
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST.get("email")]
            event = Event.objects.filter(organizer=request.user).last()
            subject =f'Invitation for {event.name}'
            message =f"Hey, {event.organizer} has invited you to an event, {event.name}. The event is about {event.desc}. Please join by clicking here, https://127.1.1.0:8000{('event-join')}?code={event.code}"
            
            send_mail(subject, message, email_from, recipient_list ,)
            return redirect('event-email-send')
        else:
            return render(request,'events/email_form.html',context={"title":"Send an email"})

def index(request):
    return render(request,'events/index.html',context={"title":"Event-Management"})





    



        


        
        




        



