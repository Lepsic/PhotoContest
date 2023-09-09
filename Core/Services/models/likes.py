from django.db import models


class Likes(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=False)
    photo_id = models.ForeignKey('PhotoContent', on_delete=models.CASCADE)


