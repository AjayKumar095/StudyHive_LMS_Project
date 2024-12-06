from django.contrib import admin
from django.contrib.admin.sites import site
from AdminWorkFlow.models import CourseDetails
from AdminWorkFlow.models import Userquery

## Admin work

class coursedetailsAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_price', 'course_language',
                    'course_duration', 'course_startdata',  'course_description',
                    'course_long_description', 'course_thumbnail')
    

class UserqueryAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'Date', 'query_type', 'query')
    
    
admin.site.register(CourseDetails, coursedetailsAdmin)    
admin.site.register(Userquery, UserqueryAdmin)