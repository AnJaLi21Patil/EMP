from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Department, Role


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='/login/')
def all_emp(request):
    emps = Employee.objects.filter(user=request.user)
    return render(request, 'all_emp.html', {'emps': emps})


@login_required(login_url='/login/')
def add_emp(request):
    if request.method == 'POST':
        try:
            first_name = request.POST['first_name']
            last_name = request.POST.get('last_name', '')
            salary = int(request.POST.get('salary', 0))
            bonus = int(request.POST.get('bonus', 0))
            phone = int(request.POST.get('phone', 0))
            dept_name = request.POST.get('dept')
            role_name = request.POST.get('role')

            dept, _ = Department.objects.get_or_create(name=dept_name)
            role, _ = Role.objects.get_or_create(name=role_name)

            new_emp = Employee(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                bonus=bonus,
                phone=phone,
                dept=dept,
                role=role,
                hire_date=datetime.now().date()
            )
            new_emp.save()
            return HttpResponse("✅ Employee Added Successfully")

        except Exception as e:
            print("❌ Error adding employee:", e)
            return HttpResponse("❌ Error while adding employee")

    departments = Department.objects.all()
    roles = Role.objects.all()
    return render(request, 'add_emp.html', {
        'departments': departments,
        'roles': roles
    })


@login_required(login_url='/login/')
def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp = Employee.objects.get(id=emp_id, user=request.user)
            emp.delete()
            return HttpResponse("✅ Employee removed successfully")
        except Employee.DoesNotExist:
            return HttpResponse("❌ You can only remove your own employees")

    emps = Employee.objects.filter(user=request.user)
    return render(request, 'remove_emp.html', {'emps': emps})


@login_required(login_url='/login/')
def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')

        emps = Employee.objects.filter(user=request.user)
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        return render(request, 'all_emp.html', {'emps': emps})

    return render(request, 'filter_emp.html')
