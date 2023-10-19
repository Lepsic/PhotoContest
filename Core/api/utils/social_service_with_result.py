from allauth.socialaccount.forms import SignupForm
from abc import ABC


class ServiceWithResult(SignupForm, ABC):
    """
    Add result field into Service object
    """
    custom_validations = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_status = None

    def run_custom_validations(self):
        for custom_validation in self.__class__.custom_validations:
            getattr(self, custom_validation)()

