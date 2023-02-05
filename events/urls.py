from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='event-home'),
    path('about/',views.about,name="event-about"),
    path('join-event/',views.join_event,name="event-join"),
    path('create-event/',views.create_event,name='event-create'),
    path('manage-event/',views.manage_event,name='event-manage'),
    path('my_invitations/',views.my_invitations,name='event-invitations'),
    path('send_email/',views.send_email,name='event-email-send')
    
]