from django.db import models



class Likes(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    photo_id = models.ForeignKey('PhotoContent',on_delete=models.CASCADE)

    count = models.BigIntegerField(default=0)
