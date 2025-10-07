import csv

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from employees.models import Department, Employee
from employees.pagination import StandardResultsSetPagination

from .serializers import (
    DepartmentSerializer,
    EmployeeCreateSerializer,
    EmployeeListSerializer,
    EmployeeSerializer,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.filter(is_deleted=False).select_related("department")
    serializer_class = EmployeeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["department__name", "age"]
    search_fields = ["name", "email"]
    ordering_fields = ["name", "age", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == "create":
            return EmployeeCreateSerializer
        elif self.action == "list":
            return EmployeeListSerializer
        return EmployeeSerializer

    def get_queryset(self):
        """
        Optionally filter employees by department using query parameter
        Example: /api/v1/employees/?department=IT
        """
        queryset = super().get_queryset()

        # Filter by department name (for backward compatibility)
        department = self.request.query_params.get("department", None)
        if department:
            queryset = queryset.filter(department__name__iexact=department)

        return queryset

    def create(self, request, *args, **kwargs):
        """Create a new employee"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()

        # Return full employee details
        output_serializer = EmployeeSerializer(employee)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Soft delete an employee"""
        instance = self.get_object()
        instance.soft_delete()
        return Response(
            {"message": "Employee deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["get"])
    def export(self, request):
        """
        Export employees as CSV or JSON
        Example: /api/v1/employees/export/?format=csv
        Example: /api/v1/employees/export/?format=json
        """
        export_format = request.query_params.get("format", "json").lower()

        # Get filtered queryset
        queryset = self.filter_queryset(self.get_queryset())

        if export_format == "csv":
            return self._export_csv(queryset)
        else:
            return self._export_json(queryset)

    def _export_csv(self, queryset):
        """Export employees as CSV"""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="employees.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Name", "Email", "Age", "Department", "Created At"])

        for employee in queryset:
            writer.writerow(
                [
                    employee.id,
                    employee.name,
                    employee.email,
                    employee.age,
                    employee.department.name,
                    employee.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

        return response

    def _export_json(self, queryset):
        """Export employees as JSON"""
        serializer = EmployeeListSerializer(queryset, many=True)
        return Response({"count": queryset.count(), "employees": serializer.data})


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Department operations
    """

    queryset = Department.objects.filter(is_deleted=False)
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering = ["name"]

    def destroy(self, request, *args, **kwargs):
        """Soft delete a department"""
        instance = self.get_object()

        # Check if department has employees
        if instance.employee_count > 0:
            return Response(
                {"error": "Cannot delete department with existing employees"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.is_deleted = True
        instance.save()
        return Response(
            {"message": "Department deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
