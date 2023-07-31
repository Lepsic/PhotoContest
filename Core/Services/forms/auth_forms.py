from django import forms
from ..service.auth import ServiceCreationUser


class UserCreationsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ServiceCreationUser(form=self)

    username = forms.CharField(max_length=40, label='Имя пользователя')
    name = forms.CharField(max_length=100, label='Имя')
    pas1 = forms.CharField(max_length=40)
    pas2 = forms.CharField(max_length=40)


    def clean(self):
        cleaned_data = super().clean()
        self.service.set_data(data=cleaned_data)
        self.service.validate_all()

