from django.contrib import admin
from django.contrib.admin.sites import site
from AdminWorkFlow.models import CourseDetails
from AdminWorkFlow.models import Userquery
from AdminWorkFlow.models import Add_Assignment
from AdminWorkFlow.models import Add_Video
from AdminWorkFlow.models import Assignment_submit
from AdminWorkFlow.models import course_purchase_by_user

## Admin work

## course details
@admin.register(CourseDetails)
class coursedetailsAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_price', 'course_language',
                    'course_duration', 'course_startdata',  'course_description',
                    'course_long_description', 'course_thumbnail')
    search_fields = ('course_title',)

## user query
@admin.register(Userquery)
class UserqueryAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'Date', 'query_type', 'query')
    search_fields = ('username', 'Date', 'query_type')

## course purchase
@admin.register(course_purchase_by_user)
class course_purchase_by_userAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'price', 'purchase_date')
    search_fields = ('course',)


# Register the Video model
@admin.register(Add_Video)
class Add_VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_at')
    list_filter = ('course',)
    search_fields = ('title',)

    # Add the course dropdown to the video upload form
    fieldsets = (
        (None, {
            'fields': ('title', 'file', 'course'),
        }),
    )

# Register the Assignment model
@admin.register(Add_Assignment)
class Add_AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_at', 'marks')
    list_filter = ('course',)
    search_fields = ('title',)
    list_editable = ('marks',)
    # Add the course dropdown to the assignment upload form
    fieldsets = (
        (None, {
            'fields': ('title', 'file', 'course'),
        }),
    )


@admin.register(Assignment_submit) 
class Assignment_submit_admin(admin.ModelAdmin):
        list_display = ('user', 'course', 'title', 'uploaded_at', 'obtained_marks')
        search_fields = ('user', 'course', 'title')
        list_editable = ('obtained_marks', )
        
        
