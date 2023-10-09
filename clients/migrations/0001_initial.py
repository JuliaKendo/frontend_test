# Generated by Django 4.1.7 on 2023-10-09 10:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('organization', models.CharField(db_index=True, default='', max_length=150, verbose_name='Организация')),
                ('inn', models.CharField(db_index=True, max_length=12, verbose_name='ИНН')),
                ('name_of_manager', models.CharField(blank=True, max_length=150, verbose_name='ФИО менеджера клиента')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='email менеджера клиента')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None, verbose_name='Телефон менеджера клиента')),
                ('status', models.CharField(choices=[('pending', 'Ожидает рассмотрения'), ('considered', 'Рассматривается'), ('registered', 'Зарегистрирован')], default='pending', max_length=10, verbose_name='Статус регистрации')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Заявка на регистрацию',
                'verbose_name_plural': 'Заявки на регистрацию',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Организация')),
                ('inn', models.CharField(db_index=True, max_length=12, verbose_name='ИНН')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(db_index=True, default=datetime.datetime.now, verbose_name='Дата обновления')),
                ('status', models.CharField(choices=[('active', 'Активный'), ('locked', 'Заблокирован')], default='active', max_length=10, verbose_name='Статус')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_clients', to=settings.AUTH_USER_MODEL, verbose_name='Утвержден')),
                ('registration_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to='clients.registrationorder', verbose_name='Заявка на регистрацию')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_clients', to=settings.AUTH_USER_MODEL, verbose_name='Изменен')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ('name',),
            },
        ),
    ]