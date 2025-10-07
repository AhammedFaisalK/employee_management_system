from django.contrib import admin
from django.urls import path, include
from employees.api.v1 import urls as employee_api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/employees/', include(employee_api_urls, namespace="api_v1_employees")),
]
