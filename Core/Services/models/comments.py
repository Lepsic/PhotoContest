from django.db import models


class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    content = models.TextField
    type_choices = [(0, 'Photo'), (1, 'Comments')]
    entity_type = models.SmallIntegerField(choices=type_choices)


""""""