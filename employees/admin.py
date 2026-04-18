from django.contrib import admin

from .models import EmployeeProfile


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'hire_date', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'phone',
    )
