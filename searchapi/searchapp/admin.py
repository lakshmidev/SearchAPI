from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from searchapp.models import User, ApiReport
from searchapp.views import generate_report

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name',
     'last_name', 'avatar','date_joined')
    list_filter = ('username', 'is_superuser', 'is_active', 
        'email', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 
        'email', 'date_joined')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('search_keyword', 'api_call_date')
    list_filter = ('api_call_date', )
    search_fields = ('search_keyword', 'api_call_date')
                

admin.site.register(User, CustomUserAdmin)
admin.site.register(ApiReport, ReportAdmin)

#Regiter custom view in admin page
admin.site.register_view('report', view=generate_report)