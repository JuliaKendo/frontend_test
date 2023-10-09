import re
from django.conf import settings

from clients.models import Client


class AuthenticationError(Exception):
    def __str__(self):
        return 'Неверный логин или пароль'


class Login(object):

    def __init__(self, request):
        self.session = request.session
        session_login = self.session.get(settings.SESSION_LOGIN)
        if not session_login:
            session_login = self.session[settings.SESSION_LOGIN] = {}
        self.login = session_login

    def auth(self, login='', password=''):
        try:
            obj = Client.objects.get(inn=login)
            self.login['client'] = obj.id
            self.login['login'] = login
        except Client.DoesNotExist:
            raise AuthenticationError


    def cahnge_pass_and_auth(self, login='', password='', new_password=''):
        try:
            obj = Client.objects.get(inn=login)
            self.login['client'] = obj.id
            self.login['login'] = login
        except Client.DoesNotExist:
            raise AuthenticationError


    def unauth(self):
        del self.session[settings.SESSION_LOGIN]
        self.session.modified = True


    def get_clients(self):
        client_id = self.login.get('client')
        if client_id:
            return Client.objects.filter(pk=client_id)

