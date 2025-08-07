from django.contrib import admin
from .models import Employee
from .models import Doctor

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department', 'date_joined')



admin.site.register(Doctor)
