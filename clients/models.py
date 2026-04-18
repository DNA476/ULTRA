from django.db import models


class Client(models.Model):
    name = models.CharField('Название / имя заказчика', max_length=150)
    contact_person = models.CharField('Контактное лицо', max_length=120, blank=True)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    email = models.EmailField('Email', blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    notes = models.TextField('Заметки', blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'
        ordering = ['name']

    def __str__(self):
        return self.name
