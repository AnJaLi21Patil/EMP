from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),          # root '/'
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('all_emp/', views.all_emp, name='all_emp'),
    path('add_emp/', views.add_emp, name='add_emp'),
    path('remove_emp/', views.remove_emp, name='remove_emp'),
    path('remove_emp/<int:emp_id>/', views.remove_emp, name='remove_emp_with_id'),
    path('filter_emp/', views.filter_emp, name='filter_emp'),
]
