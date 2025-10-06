from django.contrib import admin
from . models import Employee, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for Department model"""
    list_display = ['name', 'employee_count', 'created_at', 'is_deleted']
    list_filter = ['is_deleted', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin interface for Employee model"""
    list_display = ['name', 'email', 'age', 'department', 'created_at', 'is_deleted']
    list_filter = ['department', 'is_deleted', 'created_at', 'age']
    search_fields = ['name', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'age')
        }),
        ('Department', {
            'fields': ('department',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Include soft-deleted records in admin"""
        return Employee.objects.all().select_related('department')