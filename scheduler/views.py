from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.urls import reverse
from datetime import date, timedelta
from calendar import monthrange
from .models import Employee, Site, Duty
from .forms import EmployeeForm, SiteForm, DutyForm, DutySingleForm


def index(request):
    """Головна сторінка - графік чергувань"""
    duties = Duty.objects.select_related('employee', 'site').order_by('-date')
    return render(request, 'index.html', {'duties': duties})


def add_duty(request):
    """Додавання нового чергування"""
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        site_id = request.POST.get('site_id')
        start_date = date.fromisoformat(request.POST.get('start_date'))
        end_date = date.fromisoformat(request.POST.get('end_date'))
        notes = request.POST.get('notes', '')

        # Створюємо чергування для кожного дня в діапазоні
        current_date = start_date
        while current_date <= end_date:
            try:
                Duty.objects.create(
                    employee_id=employee_id,
                    site_id=site_id,
                    date=current_date,
                    notes=notes
                )
            except Exception:
                # Ignore duplicate entries
                pass
            current_date += timedelta(days=1)

        return redirect('index')

    employees = Employee.objects.all()
    sites = Site.objects.all()
    return render(request, 'add_duty.html', {'employees': employees, 'sites': sites})


def delete_duty(request, id):
    """Видалення чергування"""
    duty = get_object_or_404(Duty, id=id)
    duty.delete()
    return redirect('index')


def change_duty_site(request):
    """Зміна об'єкта в чергуванні"""
    if request.method == 'POST':
        duty_id = request.POST.get('duty_id')
        site_id = request.POST.get('site_id')
        year = request.POST.get('year')
        month = request.POST.get('month')
        
        duty = get_object_or_404(Duty, id=duty_id)
        duty.site_id = site_id
        duty.save()
        
        return redirect('calendar_view', year=int(year), month=int(month))
    
    return redirect('index')


def employees(request):
    """Список працівників"""
    employees = Employee.objects.annotate(duty_count=models.Count('duties'))
    return render(request, 'employees.html', {'employees': employees})


def add_employee(request):
    """Додавання працівника"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})


def edit_employee(request, id):
    """Редагування працівника"""
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})


def delete_employee(request, id):
    """Видалення працівника"""
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('employees')


def sites(request):
    """Список об'єктів"""
    sites = Site.objects.annotate(duty_count=models.Count('duties'))
    return render(request, 'sites.html', {'sites': sites})


def add_site(request):
    """Додавання об'єкта"""
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sites')
    else:
        form = SiteForm()
    return render(request, 'add_site.html', {'form': form})


def edit_site(request, id):
    """Редагування об'єкта + додавання чергувань"""
    site = get_object_or_404(Site, id=id)
    
    if request.method == 'POST':
        if 'add_duty' in request.POST:
            # Додавання чергування
            employee_id = request.POST.get('employee_id')
            duty_date = date.fromisoformat(request.POST.get('date'))
            notes = request.POST.get('notes', '')
            try:
                Duty.objects.create(
                    employee_id=employee_id,
                    site_id=site.id,
                    date=duty_date,
                    notes=notes
                )
            except Exception:
                pass
        else:
            # Редагування об'єкта
            form = SiteForm(request.POST, instance=site)
            if form.is_valid():
                form.save()
                return redirect('sites')
    else:
        form = SiteForm(instance=site)
    
    employees = Employee.objects.order_by('name')
    duties = Duty.objects.filter(site=site).select_related('employee').order_by('date')
    
    return render(request, 'edit_site.html', {
        'form': form,
        'site': site,
        'employees': employees,
        'duties': duties
    })


def delete_site(request, id):
    """Видалення об'єкта"""
    site = get_object_or_404(Site, id=id)
    site.delete()
    return redirect('sites')


def calendar_view(request, year=None, month=None):
    """Календарний вигляд"""
    today = date.today()
    
    if year is None or month is None:
        year = today.year
        month = today.month
    
    # Назви місяців українською
    month_names_uk = [
        'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
        'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'
    ]
    month_name = month_names_uk[month - 1]
    
    # Кількість днів у місяці
    days_in_month = monthrange(year, month)[1]
    
    # Отримуємо всіх працівників
    employees = Employee.objects.order_by('last_name')
    
    # Отримуємо всі чергування за цей місяць
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    duties = Duty.objects.filter(
        date__gte=start_date,
        date__lt=end_date
    ).select_related('employee', 'site')
    
    # Створюємо словник для швидкого доступу до чергувань
    # Ключ: employee_id, Значення: словник {day: [(duty_id, site)]}
    duty_dict = {}
    for duty in duties:
        day = duty.date.day
        if duty.employee_id not in duty_dict:
            duty_dict[duty.employee_id] = {}
        if day not in duty_dict[duty.employee_id]:
            duty_dict[duty.employee_id][day] = []
        duty_dict[duty.employee_id][day].append((duty.id, duty.site))
    
    # Отримуємо посади для кожного працівника
    employee_positions = {e.id: e.position for e in employees}
    
    # Обчислюємо попередній та наступний місяці
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    context = {
        'year': year,
        'month': month,
        'month_name': month_name,
        'days_in_month': days_in_month,
        'employees': employees,
        'duty_dict': duty_dict,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'all_sites': Site.objects.order_by('name'),
    }
    
    return render(request, 'calendar.html', context)
