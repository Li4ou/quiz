from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django import forms

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "input100", "placeholder":"Логин пользователя",}), error_messages={'required': ''})
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "input100", "placeholder":"Имя пользователя",}), error_messages={'required': ''})
    password = forms.CharField(widget=forms.TextInput(attrs={"class": "input100", "placeholder":"Пароль","type":"password"}), error_messages={'required': ''})


    class Meta:
        model = User
        fields = ('username', 'first_name','password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:

            # Method inherited from BaseForm
            self.add_error('password', error)
        return password
