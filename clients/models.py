import datetime
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.conf import settings


class RegistrationOrder(models.Model):
    name = models.CharField('Имя', max_length=150)
    organization = models.CharField('Организация', max_length=150, db_index=True, default='')
    inn = models.CharField('ИНН', max_length=12, db_index=True)
    name_of_manager = models.CharField('ФИО менеджера клиента', max_length=150, blank=True)
    email = models.EmailField('email менеджера клиента', db_index=True)
    phone = PhoneNumberField('Телефон менеджера клиента', db_index=True)
    status = models.CharField(
        'Статус регистрации', max_length=10, default='pending', choices=(
            ('pending'   , 'Ожидает рассмотрения'),
            ('considered', 'Рассматривается'),
            ('registered', 'Зарегистрирован')
    ))
    created_at = models.DateTimeField(
        'Дата создания', db_index=True, auto_now_add=True
    )

    class Meta:
        verbose_name = 'Заявка на регистрацию'
        verbose_name_plural = 'Заявки на регистрацию'
    
    def __str__(self):
        return self.organization


class Client(models.Model):
    name = models.CharField('Организация', max_length=150)
    inn = models.CharField('ИНН', max_length=12, db_index=True)
    registration_order = models.ForeignKey(
        RegistrationOrder,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Заявка на регистрацию',
        related_name='clients'
    )
    created_at = models.DateTimeField(
        'Дата создания', db_index=True, auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления', db_index=True, default=datetime.datetime.now
    )
    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Утвержден',
        related_name='approved_clients'
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Изменен',
        related_name='updated_clients'
    )
    status = models.CharField(
        'Статус', max_length=10, default='active', choices=(
            ('active'   , 'Активный'),
            ('locked', 'Заблокирован')
    ))

    class Meta:
        ordering = ('name', )
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    
    def __str__(self):
        return f'{self.name} ({self.inn})'

