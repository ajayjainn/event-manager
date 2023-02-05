from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render , redirect
from django.contrib import messages
from .forms import UserRegisterForm
def signup(request) :
    if request.method == 'POST' :
            form = UserRegisterForm(request.POST)
            if form.is_valid() :
                form.save()
                username = form.cleaned_data.get('username') 
                messages.success(request , f'Your account has been created ! you are now able to log in {username} !') 
                return redirect('login')
    else :
            form = UserRegisterForm()  
    return render(request , 'users/register.html' , {'form' : form})



