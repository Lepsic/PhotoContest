import re
from api.utils.service_with_result import ServiceWithResult
from django import forms
from Services.models.custom_user import CustomUser


class RegistrationUserService(ServiceWithResult):

    custom_validations = ['_validate_username', '_validate_password']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_user()
        return self

    username = forms.CharField(max_length=40, label='Имя пользователя')
    name = forms.CharField(max_length=100, label='Имя')
    pas1 = forms.CharField(max_length=40, widget=forms.PasswordInput)
    pas2 = forms.CharField(max_length=40, widget=forms.PasswordInput)

    def _validate_username(self):
        username_field = 'username'
        try:
            username = self.cleaned_data.get('username')
            if re.match("^[a-zA-Z0-9_]*$", username):
                if CustomUser.objects.filter(username=username).exists():
                    self.add_error(username_field, 'Это имя пользователя уже занято, введите другое')
                if len(username) < 3:
                    self.add_error(username_field, 'Имя пользователя должно состоять из более чем 3 символов')

            else:
                self.add_error(username_field, "Используйте только допустимые символы")
        except Exception:
            self.add_error(username_field, 'Это имя пользователя уже занято, введите другое')

    def _validate_password(self):
        password_field1 = 'pas1'
        password_field2 = 'pas2'
        pas1 = self.cleaned_data.get(password_field1)
        pas2 = self.cleaned_data.get(password_field2)
        if len(pas1) < 5:
            self.add_error(password_field1, 'Пароль должен быть длиннее 10 символов')
        if pas1 != pas2:
            self.add_error(password_field2, 'Пароли должны совпадать')



    def _create_user(self):
        user = CustomUser.objects.create_user(username=self.cleaned_data['username'],
                                              password=self.cleaned_data['pas1'],
                                              first_name=self.cleaned_data['name'])
        user.save()
