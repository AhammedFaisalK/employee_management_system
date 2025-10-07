from rest_framework import serializers

from employees.models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model"""

    employee_count = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "description",
            "employee_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model with nested department"""

    department_name = serializers.CharField(source="department.name", read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(is_deleted=False),
        source="department",
        write_only=True,
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "email",
            "age",
            "department_id",
            "department_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_age(self, value):
        """Validate age is within reasonable range"""
        if value < 18:
            raise serializers.ValidationError("Employee must be at least 18 years old")
        if value > 100:
            raise serializers.ValidationError("Please enter a valid age")
        return value

    def validate_email(self, value):
        """Validate email uniqueness excluding soft-deleted records"""
        instance = self.instance
        queryset = Employee.objects.filter(email=value, is_deleted=False)

        if instance:
            queryset = queryset.exclude(id=instance.id)

        if queryset.exists():
            raise serializers.ValidationError("Employee with this email already exists")

        return value


class EmployeeCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating employees"""

    department = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ["name", "email", "age", "department"]

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Employee must be at least 18 years old")
        if value > 100:
            raise serializers.ValidationError("Please enter a valid age")
        return value

    def create(self, validated_data):
        department_name = validated_data.pop("department")

        # Get or create department
        department, _ = Department.objects.get_or_create(
            name=department_name,
            defaults={"description": f"{department_name} Department"},
        )

        validated_data["department"] = department
        return Employee.objects.create(**validated_data)


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing employees"""

    department = serializers.CharField(source="department.name")

    class Meta:
        model = Employee
        fields = ["id", "name", "email", "age", "department"]
