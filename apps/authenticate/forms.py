from django import forms
from .models import UserProfileInfo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'Password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'Repita su password'}))

    class Meta():
        model = User
        fields = ('username','password','email', 'first_name')
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Nombre'}),
            'username': forms.TextInput(
                attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Email'}),
        }
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
          self.add_error('confirm_password', "Su contraseña no coincide")


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
      model = UserProfileInfo
      fields = ('date_birth','profile_image')
      widgets = {
        'date_birth': forms.DateInput(attrs={'placeholder':'Fecha nacimiento', 'id':'datetimepicker1'})
      }

class LoginForm(forms.Form):

  username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
      'type': 'text',
      'placeholder': 'Nombre de usuario',
    }))
  password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
      'type': 'password',
      'placeholder': 'Password'
    }))

  def clean(self):
    user_found = User.objects.filter(username = self.cleaned_data['username']).exists()
    if not user_found:
      self.add_error('username', 'Username y/o password no encontrados')
    else:
      user = User.objects.get(username = self.cleaned_data['username'])
      if not user.check_password(self.cleaned_data['password']):
        self.add_error('username', 'Password incorrecto')