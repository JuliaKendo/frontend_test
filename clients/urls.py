from django.urls import path

from . import views

app_name = "clients"

urlpatterns = [
    path('reg_request/'          , views.register, name='reg_request'),
    path('reg_request_confirm/'  , views.register_confirm, name='reg_request_confirm'),
    path('login/'                , views.login, name='login'),
]
