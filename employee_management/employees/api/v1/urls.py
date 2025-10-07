from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet, EmployeeViewSet

app_name = "api_v1_employees"

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"departments", DepartmentViewSet, basename="department")

urlpatterns = [
    path("", include(router.urls)),
]
