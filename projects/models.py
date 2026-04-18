from django.db import models as db_models

from clients.models import Client
from employees.models import EmployeeProfile
from models_app.models import ModelCard


class Project(db_models.Model):
    class ProjectType(db_models.TextChoices):
        CASTING = 'casting', 'Кастинг'
        PHOTOSESSION = 'photosession', 'Фотосессия'
        SHOW = 'show', 'Показ'
        ADVERTISING = 'advertising', 'Реклама'

    class Status(db_models.TextChoices):
        NEW = 'new', 'Новый'
        IN_PROGRESS = 'in_progress', 'В работе'
        COMPLETED = 'completed', 'Завершен'
        CANCELED = 'canceled', 'Отменен'

    title = db_models.CharField('Название', max_length=200)
    client = db_models.ForeignKey(
        Client,
        on_delete=db_models.PROTECT,
        related_name='projects',
        verbose_name='Заказчик',
    )
    project_type = db_models.CharField(
        'Тип проекта',
        max_length=20,
        choices=ProjectType.choices,
        default=ProjectType.CASTING,
    )
    description = db_models.TextField('Описание', blank=True)
    start_date = db_models.DateField('Дата начала')
    end_date = db_models.DateField('Дата окончания', null=True, blank=True)
    status = db_models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    budget = db_models.DecimalField(
        'Бюджет / выручка',
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    responsible_employee = db_models.ForeignKey(
        EmployeeProfile,
        on_delete=db_models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        verbose_name='Ответственный сотрудник',
    )
    models = db_models.ManyToManyField(
        ModelCard,
        through='Participation',
        related_name='projects',
        verbose_name='Модели',
        blank=True,
    )
    notes = db_models.TextField('Заметки', blank=True)
    created_at = db_models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = db_models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-start_date', 'title']

    def __str__(self):
        return self.title


class Participation(db_models.Model):
    class Status(db_models.TextChoices):
        INVITED = 'invited', 'Приглашена'
        UNDER_REVIEW = 'under_review', 'На рассмотрении'
        APPROVED = 'approved', 'Утверждена'
        REJECTED = 'rejected', 'Отказ'
        COMPLETED = 'completed', 'Завершено'

    project = db_models.ForeignKey(
        Project,
        on_delete=db_models.CASCADE,
        related_name='participations',
        verbose_name='Проект',
    )
    model = db_models.ForeignKey(
        ModelCard,
        on_delete=db_models.CASCADE,
        related_name='participations',
        verbose_name='Модель',
    )
    status = db_models.CharField(
        'Статус участия',
        max_length=20,
        choices=Status.choices,
        default=Status.INVITED,
    )
    comment = db_models.TextField('Комментарий', blank=True)
    assigned_at = db_models.DateTimeField('Дата назначения', auto_now_add=True)

    class Meta:
        verbose_name = 'Участие модели в проекте'
        verbose_name_plural = 'Участия моделей в проектах'
        ordering = ['-assigned_at']
        constraints = [
            db_models.UniqueConstraint(
                fields=['project', 'model'],
                name='unique_model_participation_per_project',
            ),
        ]

    def __str__(self):
        return f'{self.model} - {self.project}'
