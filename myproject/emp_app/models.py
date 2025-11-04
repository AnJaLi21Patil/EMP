# # from django.db import models

# # # Create your models here.
# # class department(models.Model):
# #     name=models.CharField(max_length=100, null=False)
# #     location = models.CharField(max_length=100)
 
# #     def __str__(self):
# #      return self.name
 

# # class Role(models.Model):
# #     name =models.CharField( max_length=50, null=False)
# #     def __str__(self):
# #      return self.name


# # class Employee(models.Model):
# #     first_name=models.CharField(max_length=100, null=False)
# #     last_name=models.CharField(max_length=100)
# #     dept = models.ForeignKey(department, on_delete=models.CASCADE)
# #     salary=models.IntegerField(default=0)
# #     bonus=models.IntegerField(default=0)
# #     role=models.ForeignKey(Role, on_delete=models.CASCADE)
# #     phone=models.IntegerField(default=0)
# #     hire_date=models.DateField()

# #     def __str__(self):
# #         return "%s %s %s " %(self.first_name, self.last_name, self.phone)
        

# from django.db import models
# from django.contrib.auth.models import User  # Add this import

# class Department(models.Model):
#     name = models.CharField(max_length=100, null=False)
#     location = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


# class Role(models.Model):
#     name = models.CharField(max_length=50, null=False)

#     def __str__(self):
#         return self.name


# class Employee(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # <-- New field
#     first_name = models.CharField(max_length=100, null=False)
#     last_name = models.CharField(max_length=100)
#     dept = models.ForeignKey(Department, on_delete=models.CASCADE)
#     salary = models.IntegerField(default=0)
#     bonus = models.IntegerField(default=0)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
#     phone = models.IntegerField(default=0)
#     hire_date = models.DateField()

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.phone})"
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # who added this record
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, blank=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.BigIntegerField(default=0)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"
