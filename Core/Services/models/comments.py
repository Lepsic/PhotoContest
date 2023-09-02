from django.db import models


class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('CustomUser', on_delete=models.DO_NOTHING)

    content = models.TextField(blank=True)
    type_choices = [(0, 'Photo'), (1, 'Comments')]
    entity_type = models.SmallIntegerField(choices=type_choices)
    parent_id_image = models.ForeignKey('PhotoContent', on_delete=models.CASCADE)
    parent_id_comments = models.ForeignKey('Comments', on_delete=models.DO_NOTHING, null=True)
    create_time = models.DateField(blank=True)