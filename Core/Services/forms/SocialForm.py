from allauth.socialaccount.forms import SignupForm, BaseSignupForm
from django import forms
from Services.service.auth.service_social_registrtation import RegistrationSocialService







class MyCustomSocialSignupForm(SignupForm, RegistrationSocialService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        fields = ['username', 'pas1', 'pas2']


    username = forms.CharField(max_length=40, label='Имя пользователя')
    pas1 = forms.CharField(max_length=40, widget=forms.PasswordInput, label='Пароль')
    pas2 = forms.CharField(max_length=40, widget=forms.PasswordInput, label='Подтвердите пароль')

    def clean(self):
        self.process()


    def save(self, request):
        if self.result is True:
            user = super().save(request)
            return user
