from django.conf import settings
from django.db import models


class EmployeeProfile(models.Model):
    class Role(models.TextChoices):
        DIRECTOR = 'director', 'Директор агентства'
        BOOKER = 'booker', 'Букер'
        SCOUT = 'scout', 'Скаут'
        ADMIN = 'admin', 'Системный администратор'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        verbose_name='Пользователь',
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=Role.choices,
        default=Role.SCOUT,
    )
    phone = models.CharField('Телефон', max_length=30, blank=True)
    hire_date = models.DateField('Дата приема', null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Профиль сотрудника'
        verbose_name_plural = 'Профили сотрудников'
        ordering = ['user__last_name', 'user__first_name', 'user__username']

    def __str__(self):
        full_name = self.user.get_full_name()
        return full_name or self.user.get_username()
