from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_duty/', views.add_duty, name='add_duty'),
    path('delete_duty/<int:id>/', views.delete_duty, name='delete_duty'),
    path('change_duty_site/', views.change_duty_site, name='change_duty_site'),
    
    path('employees/', views.employees, name='employees'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('edit_employee/<int:id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    
    path('sites/', views.sites, name='sites'),
    path('add_site/', views.add_site, name='add_site'),
    path('edit_site/<int:id>/', views.edit_site, name='edit_site'),
    path('delete_site/<int:id>/', views.delete_site, name='delete_site'),
    
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_view'),
]
