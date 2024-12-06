from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import aauthenticate, login, logout
from  django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from AdminWorkFlow.models import CourseDetails, course_purchase_by_user


## index page
def index(request):
    coursedetails = CourseDetails.objects.all()
    return render(request=request, template_name="index.html",  context={"coursedetails": coursedetails})

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
               
## course information page
def course_info(request):
    try:
        if request.method == 'POST':
            course_id = int(request.POST.get('course_id'))
            current_course = CourseDetails.objects.get(id=course_id)
            current_course_data = {
                'course_info' : current_course 
            }
    
            return render(request=request, template_name='CourseInfo.html', context=current_course_data)
        
        else:
            return HttpResponse('Something going wrong')
    
    except Exception as e:
        return HttpResponse(f'Error {e}')                  
                
## course purchase :
def purchase_course(request):
    
    try:
        if request.method == "POST":
            
            ## chech the user is logged in or not.
            if not request.user.is_authenticated:
                return redirect('user')
            
            course_id = int(request.POST.get('course_id'))
            print(f'Course id = {course_id} and type of = {type(course_id)}')
            course = get_object_or_404(CourseDetails, id=course_id)
            print(f'course get = { course}')
            ## check if user already purchase the course or not
            if course_purchase_by_user.objects.filter(user=request.user, course =course).exists():
                return HttpResponse('You have already purchased this course!')
            
            # create a new purchaase entry 
            course_purchase_by_user.objects.create(
                user=request.user,
                course = course,
                price = course.course_price
            )
        
            return redirect('mycourses')
        else :
            return HttpResponse('Error while purchasing course')   
    
    except Exception as e:
        return HttpResponse(f'Error {e}')  

## my course page
def mycourse(request):
    try:
        if not request.user.is_authenticated:
            return redirect('user')
        
        user_id = request.user.id
        my_purchase = course_purchase_by_user.objects.filter(user_id=user_id)
        for data in my_purchase:
            print(" details = ",data.user_id)
            print(" details = ",data.course_id)
        return HttpResponse(f'we got data sucessfully.')
    except Exception as e:
        return HttpResponse(f'Error {e}')