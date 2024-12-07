from django.contrib import admin
from django.contrib.admin.sites import site
from AdminWorkFlow.models import CourseDetails
from AdminWorkFlow.models import Userquery
from AdminWorkFlow.models import course_purchase_by_user

## Admin work

class coursedetailsAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_price', 'course_language',
                    'course_duration', 'course_startdata',  'course_description',
                    'course_long_description', 'course_thumbnail')
    

class UserqueryAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'Date', 'query_type', 'query')


class course_purchase_by_userAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'price', 'purchase_date')

   
admin.site.register(course_purchase_by_user, course_purchase_by_userAdmin)  
admin.site.register(CourseDetails, coursedetailsAdmin)    
admin.site.register(Userquery, UserqueryAdmin)