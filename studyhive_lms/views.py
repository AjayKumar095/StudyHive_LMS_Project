from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  login, logout
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from AdminWorkFlow.models import CourseDetails
from AdminWorkFlow.models import course_purchase_by_user
from AdminWorkFlow.models import Userquery
from AdminWorkFlow.models import Assignment_submit
from AdminWorkFlow.models import Add_Assignment
import base64
import os

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
            
            ## check for username lenght 
            if len(username) > 15 :
                messages.warning( request,'Username length is too long. Max lenght 15 characters.')
                return redirect('user')
            
        # Check if passwords match
            if password == password_conf:
            # Check if username already exists
                user = User.objects.filter(username=username).first()  # safer than using get()
                if user:
                    messages.warning(request, 'The username already exists. Please choose a different username, or if you already have an account, you can log in.')
                    return redirect('user')
                
                validate_password(password=password)
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Account created successfully!')
                return redirect('user')  # Redirect to login page after successful signup
            else:
                messages.warning(request, 'Passwords do not match.')
                return redirect('user')
   
    except ValidationError as e:
        for error in e.messages:
            messages.warning(request, error)
            return redirect('user')
        
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
                messages.warning(request,'Username does not exists. Check the username or create an account.')
                return redirect('user')
                
            
            if user and check_password(login_password, user.password):
                login(request=request, user=user)
                return redirect('index')
            
            else:
                messages.warning(request, 'Invaid username and passeord.')
                return redirect('user')
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
           
            course = get_object_or_404(CourseDetails, id=course_id)
        
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
        
        course_id_list=[]
        for data in my_purchase:
            course_id_list.append(data.course_id)
            
        purchased_courses = CourseDetails.objects.filter(id__in=course_id_list)
        
        purchased_courses_data = {
            'purchased_courses': purchased_courses
        }
        
        return render(request=request, template_name='my_course.html', context=purchased_courses_data)
    
    except Exception as e:
        return HttpResponse(f'Error {e}')

## my profile page
def myprofile(request):
    try:
        if not request.user.is_authenticated:
            return redirect('user')
        
        return render(request=request, template_name='My_profile.html')
        
    except Exception as e :
        return HttpResponse(f'Error {e}')

## delete user and his/her data.
def deleteuser(request):
    try:
        if not request.user.is_authenticated:
            return redirect('user')
        
        if request.method == "POST":
            username = request.POST.get('to_delete_user')
            User.objects.filter(username=username).delete()
            return redirect('index')
        else:
            return HttpResponse('error while deleting user.')
        
    except Exception as e:
        return HttpResponse(f'Error {e}')

## user help page.
def userhelp(request):
    try:
        if not request.user.is_authenticated:
            return redirect('user')
        
        return render(request=request, template_name='support_page.html')
    
    except Exception as e:
        return HttpResponse(f'Error {e}')
        
## user support page
def userquery(request):
    
    try:
        if not request.user.is_authenticated:
            return redirect('user')
        
        if request.method == "POST":
            
            username = request.POST.get('Username')  
            email = request.POST.get('UserEmail')
            query_type = request.POST.get('Querytype')
            query = request.POST.get('UserQuery') 
            
            Userquery.objects.create(
                username=username,
                email=email,
                query_type=query_type,
                query=query
            )
            messages.success(request, 'Your query has been submitted. We will reach you within 24 hours.')

            return redirect('userhelp')
        
        else:
            return HttpResponse("Error while collecting the user query")     
    
    except Exception as e:
        return HttpResponse(f'Error {e}')

## course view
def course_view(request):
    try:
        
        if not request.user.is_authenticated:
            messages.warning(request=request, message='Login to your account to access the course content.')
            return redirect('user')
        
        if request.method == "POST":
            course_id = request.POST.get('course_id')
            course = CourseDetails.objects.get(id=course_id)
            videos = course.videos.all()
            assignment = course.assignments.all()
            
            assignment_list = [ ] 
            for file_path in assignment:
                
                submit_assignment = Assignment_submit.objects.get(course_id=course_id, title=file_path.title, user_id = request.user)
                file_string=pdf_to_string(file_path.file)
                assignment_list.append({file_path.title: [file_string, file_path.marks, submit_assignment.obtained_marks]})
            
            
            course_content = {
                'Videos':videos,
                'Assignments':assignment_list,
                'course':course
                
            }
            #print(assignment_list)
            return render(request=request, template_name="course_content_view.html",context=course_content)  #context=course_content          
        else:
            course_id = request.session.get('course_id', None)
            print(f'course_id in course view function: {course_id}, and type of this id {type(course_id)}')
            course = CourseDetails.objects.get(id=course_id)
            videos = course.videos.all()
            assignment = course.assignments.all()
            
            assignment_list = [ ] 
            for file_path in assignment:
                
                submit_assignment = Assignment_submit.objects.get(course_id=course_id, title=file_path.title, user_id = request.user)
                file_string=pdf_to_string(file_path.file)
                assignment_list.append({file_path.title: [file_string, file_path.marks, submit_assignment.obtained_marks]})
            
            
            course_content = {
                'Videos':videos,
                'Assignments':assignment_list,
                'course':course
                
            }
            return render(request=request, template_name="course_content_view.html",context=course_content)            
    
    except Exception as e:
        messages.error(request=request, message=e)
        return redirect('mycourses')

## Assignment submit module
def uploaded_assignment(request):
    
    try:
        if request.method == "POST":
            # Get the uploaded file and title from the form
            pdf_file = request.FILES.get('pdf_file')
            assignment_title = request.POST.get('pdf_title')
            course_id = request.POST.get('course_id')
            print(f'course_id in assignment function: {course_id}, and type of this id {type(course_id)}')
            
            print(f'assignment title:  {assignment_title}, pdf file = {pdf_file}')
            
            # Validate that both file and title are provided
            if not pdf_file or not assignment_title:
                return JsonResponse({'status': 'error', 'message': 'Assignment title and file are required.'})

            try:
                # Fetch the related assignment and course details
                assignment = Add_Assignment.objects.filter(title=assignment_title).first()
                if not assignment:
                    return JsonResponse({'status': 'error', 'message': 'Assignment not found.'})

                course = assignment.course  # Retrieve the related course from the assignment
                user = request.user  # Get the currently logged-in user
            except CourseDetails.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Course not found for the provided title.'})

            # Check if an existing assignment for the user and course already exists
            existing_assignment = Assignment_submit.objects.filter(user=user, course=course).first()

            if existing_assignment:
                # Delete the old file and update the record
                existing_assignment.pdf_file.delete()  # Remove the old file from storage
                existing_assignment.pdf_file = pdf_file
                existing_assignment.save()
            else:
                # Create a new assignment record
                Assignment_submit.objects.create(
                    title=assignment_title,
                    pdf_file=pdf_file,
                    user=user,
                    course=course,
                )

            
            request.session['course_id'] = int(course_id)
            return redirect('course_view')  # Redirect to the course view or any relevant page

    except Exception as e:
        return HttpResponse(f'Error: {e}')



## pdf to string
def pdf_to_string(path):

    try:
        file_path = os.path.join('media', str(path))
        with open(file=file_path, mode='rb') as pdf_file:
                
            pdf_content = base64.b64encode(pdf_file.read()).decode()
                
            return pdf_content
          
    except:
        print('path not get')
        return None     