from allauth.socialaccount.forms import SignupForm, BaseSignupForm
from django import forms
from Services.service.auth.service_creation_user import SaveUser
from Services.service.auth.service_validate import ServiceValidateUserData





class MyCustomSocialSignupForm(SignupForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ServiceValidateUserData(form=self)

    class Meta:
        fields = ['username', 'pas1', 'pas2']


    username = forms.CharField(max_length=40, label='Имя пользователя')
    pas1 = forms.CharField(max_length=40, widget=forms.PasswordInput, label='Пароль')
    pas2 = forms.CharField(max_length=40, widget=forms.PasswordInput, label='Подтвердите пароль')

    def clean(self):
        cleaned_data = super().clean()
        self.service.run_validate()

    def save(self, request):
        user = super().save(request)
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['pas1'])
        user.save()
        return user
