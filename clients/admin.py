from django.contrib import admin
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.admin import SimpleListFilter
from django.conf import settings

from .models import (
    RegistrationOrder,
    Client
)

from .forms import CustomRegOrderForm


class RegistrationOrderFilter(SimpleListFilter):
    title = 'Статусы заявок'
    parameter_name = 'status'

    def default_value(self):
        return 'not_registered'

    def lookups(self, request, model_admin):
        return (
            ('not_registered', 'Не зарегистрированные'),
            ('registered', 'Зарегистрированные'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'not_registered':
            return queryset.filter(
                status__in=['pending', 'considered']
            )
        if self.value() == 'registered':
            return queryset.filter(status='registered')


@admin.register(RegistrationOrder)
class RegistrationOrderAdmin(admin.ModelAdmin):
    form = CustomRegOrderForm
    search_fields = [
        'name',
        'organization',
        'inn',
        'email',
        'phone',
        'status'
    ]
    list_display = [
        'name',
        'organization',
        'inn',
        'email',
        'phone',
        'status'
    ]
    list_filter = [
        'status',
    ]
    fields = [
        'status',
        'name',
        ('organization', 'inn'),
        (
            'email',
            'phone',
        ),
        ('login', 'password'),
    ]
    list_filter = (RegistrationOrderFilter,)

    def check_registration(self, obj):
        if obj:
            return obj.status == 'registered' and \
                Client.objects.filter(registration_order=obj).exists()

    def get_readonly_fields(self, request, obj=None):
        if self.check_registration(obj):
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if self.check_registration(obj):
            for fieldset in fieldsets:
                _, field_struct = fieldset
                if ('login', 'password') in field_struct['fields']:
                    field_struct['fields'].remove(('login', 'password'))
        else:
            for fieldset in fieldsets:
                _, field_struct = fieldset
                if not ('login', 'password') in field_struct['fields']:
                    field_struct['fields'].append(('login', 'password'))
   
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):

        registration_order = form.cleaned_data
        if registration_order.get('status') == 'registered':
            with transaction.atomic():
                client, created = Client.objects.get_or_create(**{
                    'name'              : registration_order['name'],
                    'inn'               : registration_order['inn'],
                    'registration_order': obj,
                    'approved_by'       : request.user,
                })

        return super().save_model(request, obj, form, change)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'inn',
        'registration_order',
        'approved_by',
        'updated_by',
    ]
    list_display = [
        'status',
        'name',
        'inn',
        'registration_order',
        'created_at',
        'approved_by',
    ]
    fields = [
        'status',
        ('name', 'inn'),
        'registration_order',
        ('created_at', 'approved_by'),
        ('updated_at', 'updated_by'),
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'registration_order',
        'approved_by',
        'updated_by',
    ]
    list_filter = [
        'status',
    ]
