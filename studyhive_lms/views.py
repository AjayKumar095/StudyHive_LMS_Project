from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import aauthenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password


## index page
def index(request):
    return render(request=request, template_name="index.html")


## user login page
def user(request):
    try:
        return render(request=request, template_name="UserLoginPage.html")
    
    except Exception as e:
        return HttpResponse(content=f"error {e}")
    
## user sign up page

def usersignup(request):
    
    try:
        if request.method == 'POST':
            username = request.POST.get('signupusername')
            email = request.POST.get('signupemail')
            password = request.POST.get('signuppassword')
            password_conf = request.POST.get('signupConfirmpassword')
            
            print( username, email,  password)
            #hash_password = make_password(password=password)
            
        # Check if passwords match
            if password == password_conf:
            # Check if username already exists
                user = User.objects.filter(username=username).first()  # safer than using get()
                if user:
                    messages.error(request, 'Username already exists.')
                    return redirect('user')

                    # Create new user if no existing user
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Account created successfully!')
                return redirect('user')  # Redirect to login page after successful signup
            else:
                messages.error(request, 'Passwords do not match.')

    except Exception as e:
        return HttpResponse(f'error {e}')                
    
## user login 
def userlogin(request):
    
    try:
        if request.method == "POST":
            login_username = request.POST.get('Username_login')
            login_password = request.POST.get('Passward_login')
           
            try :
                user = User.objects.get(username=login_username)
            except User.DoesNotExist:
                user = None
                messages.error('Username does not exists.')
                return redirect('usersignup')
                
            
            if user and check_password(login_password, user.password):
                login(request=request, user=user)
                return redirect('index')
            
            else:
                return HttpResponse('invalid username or password')
    except Exception as e:
        return HttpResponse(f'Error occure. {e}')            
            
## user logout
def userlogout(request):
    logout(request=request)
    return redirect('index')
               
                    
                
    