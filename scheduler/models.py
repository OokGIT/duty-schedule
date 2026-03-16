from django.db import models


class Employee(models.Model):
    """Модель для працівників"""
    last_name = models.CharField(max_length=50, default='', verbose_name="Прізвище")
    first_name = models.CharField(max_length=50, default='', verbose_name="Ім'я")
    patronymic = models.CharField(max_length=50, blank=True, default='', verbose_name="По-батькові")
    position = models.CharField(max_length=100, blank=True, default='', verbose_name="Посада")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'
        ordering = ['last_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}' if self.patronymic else f'{self.last_name} {self.first_name}'

    def full_name(self):
        """Повне ПІБ"""
        if self.patronymic:
            return f'{self.last_name} {self.first_name} {self.patronymic}'
        return f'{self.last_name} {self.first_name}'

    def initials(self):
        """Прізвище та ініціали"""
        initial = self.first_name[0] if self.first_name else ''
        if self.patronymic:
            initial += f'.{self.patronymic[0]}.'
        elif self.first_name:
            initial += '.'
        return f'{self.last_name} {initial}'

    def duties_count(self):
        return self.duties.count()


class Site(models.Model):
    """Модель для об'єктів"""
    name = models.CharField(max_length=100, verbose_name="Назва об'єкта")
    short_name = models.CharField(max_length=20, blank=True, verbose_name="Скорочена назва")
    address = models.CharField(max_length=200, blank=True, verbose_name="Адреса")
    display_mode = models.CharField(
        max_length=10,
        choices=[('symbol', 'Символ'), ('color', 'Кольором')],
        default='symbol',
        verbose_name="Відображення в календарі"
    )
    color = models.CharField(
        max_length=7,
        default='#4f46e5',
        verbose_name="Колір"
    )
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
