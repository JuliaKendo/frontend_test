from django import template
from django.conf import settings
from contextlib import suppress

from clients.models import Client

register = template.Library()

@register.filter
def login_info(session):
    login_name = ''
    session_login = session.get(settings.SESSION_LOGIN)
    if not session_login:
        return ''
    client_id = session_login.get('client')
    with suppress(Client.DoesNotExist):
        if client_id:
            login_name = str(Client.objects.get(pk=client_id))
        
    return login_name
