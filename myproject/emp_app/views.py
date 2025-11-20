from datetime import datetime
import requests
from django.shortcuts import render, redirect
from django.contrib import messages

API_BASE = "http://127.0.0.1:8000/api/"
REGISTER_API = f"{API_BASE}register/"
LOGIN_API = f"{API_BASE}login/"
EMP_API = f"{API_BASE}employees/"
DEPT_API = f"{API_BASE}departments/"
ROLE_API = f"{API_BASE}roles/"

# ===================== AUTHENTICATION =====================
def register(request):
    if request.method == "POST":
        data = {"username": request.POST.get("username"), "password": request.POST.get("password")}
        try:
            response = requests.post(REGISTER_API, data=data)
            if response.status_code == 201:
                messages.success(request, "✅ Registration successful. Please login.")
                return redirect("login")
            else:
                messages.error(request, response.json().get("error", "Registration failed"))
        except Exception as e:
            messages.error(request, f"API error: {e}")
    return render(request, "register.html")

def login_user(request):
    if request.method == "POST":
        data = {"username": request.POST.get("username"), "password": request.POST.get("password")}
        try:
            response = requests.post(LOGIN_API, data=data)
            if response.status_code == 200:
                request.session["user"] = data["username"]
                messages.success(request, f"✅ Login successful. Welcome {data['username']}!")
                return redirect("index")
            else:
                messages.error(request, response.json().get("error", "Login failed"))
        except Exception as e:
            messages.error(request, f"API error: {e}")
    return render(request, "login.html")

def logout_user(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect("login")

# ===================== DASHBOARD =====================
def index(request):
    if "user" not in request.session:
        return redirect("login")
    return render(request, "index.html")

# ===================== EMPLOYEE CRUD =====================
def all_emp(request):
    if "user" not in request.session:
        return redirect("login")
    try:
        response = requests.get(EMP_API)
        emps = response.json() if response.status_code == 200 else []
    except Exception as e:
        messages.error(request, f"API error: {e}")
        emps = []
    return render(request, "all_emp.html", {"emps": emps})

def add_emp(request):
    if "user" not in request.session:
        return redirect("login")

    try:
        depts = requests.get(DEPT_API).json()
        roles = requests.get(ROLE_API).json()
    except Exception as e:
        messages.error(request, f"API error: {e}")
        depts, roles = [], []

    if request.method == "POST":
        hire_date = request.POST.get("hire_date") or datetime.now().date().isoformat()
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "dept": request.POST.get("dept"),
            "role": request.POST.get("role"),
            "salary": request.POST.get("salary"),
            "bonus": request.POST.get("bonus"),
            "phone": request.POST.get("phone"),
            "hire_date": hire_date,
        }
        try:
            response = requests.post(EMP_API, data=data)
            if response.status_code in [200, 201]:
                messages.success(request, "✅ Employee added successfully.")
                return redirect("all_emp")
            else:
                messages.error(request, response.json().get("error", "Failed to add employee"))
        except Exception as e:
            messages.error(request, f"API error: {e}")

    return render(request, "add_emp.html", {"departments": depts, "roles": roles})

def remove_emp(request, emp_id):
    if "user" not in request.session:
        return redirect("login")
    try:
        response = requests.delete(f"{EMP_API}{emp_id}/")
        if response.status_code in [200, 204]:
            messages.success(request, f"✅ Employee {emp_id} removed successfully.")
        else:
            messages.error(request, "Failed to remove employee.")
    except Exception as e:
        messages.error(request, f"API error: {e}")
    return redirect("all_emp")

def filter_emp(request):
    if "user" not in request.session:
        return redirect("login")
    emps = []
    if request.method == "POST":
        search = request.POST.get("name", "")
        try:
            response = requests.get(EMP_API, params={"search": search})
            if response.status_code == 200:
                emps = response.json()
        except Exception as e:
            messages.error(request, f"API error: {e}")
    return render(request, "all_emp.html", {"emps": emps})
