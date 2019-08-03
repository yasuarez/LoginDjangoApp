from django.urls import path
from .views import *


app_name = 'authenticate'

urlpatterns = [
    path('index/', index, name="index"),
    path('register/', register, name="register"),
    path('user_login/', login_user, name="login_user"),
    path('validate/',validate_auth, name="validate_login"),
    path('logout/', user_logout, name="logout_user"),
    path('export_pdf/', export_pdf, name="export_pdf")
]