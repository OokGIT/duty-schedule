from django.db import models


class Employee(models.Model):
    """Модель для працівників"""
    name = models.CharField(max_length=100, verbose_name="Ім'я та прізвище")
    position = models.CharField(max_length=100, blank=True, verbose_name="Посада")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.position}' if self.position else self.name

    def duties_count(self):
        return self.duties.count()


class Site(models.Model):
    """Модель для об'єктів"""
    name = models.CharField(max_length=100, verbose_name="Назва об'єкта")
    short_name = models.CharField(max_length=20, blank=True, verbose_name="Скорочена назва")
    address = models.CharField(max_length=200, blank=True, verbose_name="Адреса")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Об'єкт"
        verbose_name_plural = "Об'єкти"
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.address})' if self.address else self.name

    def duties_count(self):
        return self.duties.count()


class Duty(models.Model):
    """Модель для чергувань"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='duties', verbose_name='Працівник')
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='duties', verbose_name="Об'єкт")
    date = models.DateField(verbose_name='Дата')
    notes = models.TextField(blank=True, verbose_name='Примітки')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Чергування'
        verbose_name_plural = 'Чергування'
        ordering = ['-date']
        unique_together = ['employee', 'date']

    def __str__(self):
        return f'{self.employee.name} at {self.site.name} on {self.date}'
