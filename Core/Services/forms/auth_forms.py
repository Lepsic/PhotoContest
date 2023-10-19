# from django import forms
#
# from Services.service.auth.service_validate import ServiceValidateUserData
#
#
# class UserCreationsForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.service = ServiceValidateUserData(form=self)
#
#     username = forms.CharField(max_length=40, label='Имя пользователя')
#     name = forms.CharField(max_length=100, label='Имя')
#     pas1 = forms.CharField(max_length=40, widget=forms.PasswordInput)
#     pas2 = forms.CharField(max_length=40, widget=forms.PasswordInput)
#
#
#     def clean(self):
#         self.service.run_validate()
#
