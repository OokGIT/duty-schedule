from django import forms
from .models import Employee, Site, Duty


class EmployeeForm(forms.ModelForm):
    """Форма для працівників"""
    class Meta:
        model = Employee
        fields = ['name', 'position']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: Іван Петренко"
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: Охоронець"
            }),
        }


class SiteForm(forms.ModelForm):
    """Форма для об'єктів"""
    class Meta:
        model = Site
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: Склад №1"
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: вул. Промислова, 15"
            }),
        }


class DutyForm(forms.ModelForm):
    """Форма для чергувань"""
    class Meta:
        model = Duty
        fields = ['employee', 'site', 'start_date', 'end_date', 'notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'site': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': "Додаткова інформація про чергування..."
            }),
        }

    start_date = forms.DateField(
        label='Дата початку',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label='Дата закінчення',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )


class DutySingleForm(forms.ModelForm):
    """Форма для додавання чергування на об'єкті (без кінцевої дати)"""
    class Meta:
        model = Duty
        fields = ['employee', 'date', 'notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Додаткова інформація про чергування..."
            }),
        }
