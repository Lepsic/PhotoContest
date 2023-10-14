from Services.models.custom_user import CustomUser
class SaveUser:
    def __init__(self, form):
        self._user_data_form = form


    def save_user(self):
        user_data = self._user_data_form.cleaned_data
        user = CustomUser.objects.create_user(username=user_data['username'],
                                              password=user_data['pas1'],
                                              first_name=user_data['name'])
        user.save()
