from ..models import PhotoContent

class PhotoManager:
    """Класс для взаимодействия с картинками"""
    def __init__(self, request):
        self.request = request
        self.user = request.user


    def filter_on_profile(self):
        type_filter = self.request.GET.get('filter_value')
        photos = PhotoContent.objects.filter(user_id=self.request.user)
        if type_filter is None:
            return  self.__create_response_dictionary(photos=photos)
        else:
            photos = PhotoContent.objects.filter(status=type_filter)
            return self.__create_response_dictionary(photos)

    def __create_response_dictionary(self, photos):
        response = {}
        for photo in photos:
            response.update({'name': photo.name, 'media': self.__create_url_on_media(path=photo.media)
                             'description': photo.description})
        return response

    def __create_url_on_media(self, path):
        path = "{%url {}%}".format(path)


