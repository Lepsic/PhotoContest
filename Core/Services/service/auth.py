import re

from ..models.custom_user import CustomUser


class ServiceCreationUser:
    """Вспомогательный класс для создания пользователя. Вся валидация данных тут"""
    def __init__(self, form, data=None):
        self.validate_data = None
        self.form = form

    def set_data(self, data):
        self.validate_data = data

    def __validate_username(self):
        username_field = 'username'
        username = self.validate_data.get('username')
        if re.match("^[a-zA-Z0-9_]*$", username):
            if CustomUser.objects.filter(username=username).exists():
                self.form.add_error(username_field, 'Это имя пользователя уже занято, введите другое')
            if len(username) < 3:
                self.form.add_error(username_field, 'Имя пользователя должно состоять из более чем 3 символов')

        else:
            self.form.add_error(username_field, "Используйте только допустимые символы")

    def __validate_password(self):
        password_field1 = 'pas1'
        password_field2 = 'pas2'
        pas1 = self.validate_data.get(password_field1)
        pas2 = self.validate_data.get(password_field2)
        if len(pas1) < 5:
            self.form.add_error(password_field1, 'Пароль должен быть длиннее 10 символов')
        if pas1 != pas2:
            self.form.add_error(password_field2, 'Пароли должны совпадать')

    def SaveUser(self):
        user = CustomUser.objects.create_user(username=self.validate_data['username'],
                                              password=self.validate_data['pas1'],
                                              first_name=self.validate_data['name'])
        user.save()

    def validate_all(self):
        self.__validate_username()
        self.__validate_password()
