from Services.service.auth.service_registration import RegistrationUserService


class RegistrationSocialService(RegistrationUserService):

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = True
        return self
    def _create_user(self, user):
        if self.result is True:
            user.username = self.cleaned_data['username']
            user.password = self.cleaned_data['pas1']
            user.first_name = self.cleaned_data['name']
