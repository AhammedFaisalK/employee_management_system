import uuid
from django.db import models


class BaseModel(models.Model):
    """Abstract base model with common fields for all models"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Department(BaseModel):
    """Department model to organize employees"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

    @property
    def employee_count(self):
        """Returns the count of active employees in this department"""
        return self.employees.filter(is_deleted=False).count()


class Employee(BaseModel):
    """Employee model with all required fields"""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='employees'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['department']),
            models.Index(fields=['is_deleted']),
        ]

    def __str__(self):
        return f"{self.name} - {self.department.name}"

    def soft_delete(self):
        """Soft delete the employee"""
        self.is_deleted = True
        self.save()