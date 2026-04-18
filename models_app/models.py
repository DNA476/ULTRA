from django.conf import settings
from django.db import models


class ModelCard(models.Model):
    class Category(models.TextChoices):
        TOP = 'top', 'Top-model'
        NEW_FACE = 'new_face', 'New face'
        COMMERCIAL = 'commercial', 'Commercial'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активна'
        ARCHIVED = 'archived', 'В архиве'
        ON_CONTRACT = 'on_contract', 'На контракте'

    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email', blank=True)
    city = models.CharField('Город', max_length=100)
    height = models.PositiveSmallIntegerField('Рост, см')
    bust = models.PositiveSmallIntegerField('Объем груди, см')
    waist = models.PositiveSmallIntegerField('Талия, см')
    hips = models.PositiveSmallIntegerField('Бедра, см')
    shoe_size = models.DecimalField(
        'Размер обуви',
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    hair_color = models.CharField('Цвет волос', max_length=50, blank=True)
    eye_color = models.CharField('Цвет глаз', max_length=50, blank=True)
    experience = models.TextField('Опыт работы / описание', blank=True)
    category = models.CharField(
        'Категория',
        max_length=20,
        choices=Category.choices,
        default=Category.NEW_FACE,
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_model_cards',
        verbose_name='Кем добавлена анкета',
    )
    main_photo = models.ImageField(
        'Главное фото',
        upload_to='models/main/',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Анкета модели'
        verbose_name_plural = 'Анкеты моделей'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ModelPhoto(models.Model):
    model = models.ForeignKey(
        ModelCard,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Модель',
    )
    image = models.ImageField('Фото', upload_to='models/gallery/')
    caption = models.CharField('Подпись', max_length=150, blank=True)
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Фото модели'
        verbose_name_plural = 'Фото моделей'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'Фото: {self.model}'
