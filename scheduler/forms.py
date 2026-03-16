from django import forms
from .models import Employee, Site, Duty


class EmployeeForm(forms.ModelForm):
    """Форма для працівників"""
    class Meta:
        model = Employee
        fields = ['last_name', 'first_name', 'patronymic', 'position']
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: Петренко"
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: Іван"
            }),
            'patronymic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: Іванович"
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
        fields = ['name', 'short_name', 'address', 'display_mode', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: Склад №1"
            }),
            'short_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: Склад1"
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Наприклад: вул. Промислова, 15"
            }),
            'display_mode': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'style': 'height: 40px; padding: 2px;'
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
