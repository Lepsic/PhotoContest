import re

from Services.models.custom_user import CustomUser


class ServiceValidateUserData:

    def __init__(self, form):
        self._form = form
        self._validate_data = None



    def __validate_username(self):
        try:
            username_field = 'username'
            username = self._validate_data.get('username')
            if re.match("^[a-zA-Z0-9_]*$", username):
                if CustomUser.objects.filter(username=username).exists():
                    self._form.add_error(username_field, 'Это имя пользователя уже занято, введите другое')
                if len(username) < 3:
                    self._form.add_error(username_field, 'Имя пользователя должно состоять из более чем 3 символов')

            else:
                self._form.add_error(username_field, "Используйте только допустимые символы")
        except Exception:
            self._form.add_error(username_field, 'Это имя пользователя уже занято, введите другое')

    def __validate_password(self):
        password_field1 = 'pas1'
        password_field2 = 'pas2'
        pas1 = self._validate_data.get(password_field1)
        pas2 = self._validate_data.get(password_field2)
        if len(pas1) < 5:
            self._form.add_error(password_field1, 'Пароль должен быть длиннее 10 символов')
        if pas1 != pas2:
            self._form.add_error(password_field2, 'Пароли должны совпадать')

    def run_validate(self):
        self._validate_data = self._form.cleaned_data
        self.__validate_username()
        self.__validate_password()
