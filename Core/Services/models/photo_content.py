from django.db import models


class PhotoContent(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    content_path = models.CharField(max_length=300)
    create_data = models.DateField(blank=True)  # Дата фактического создания
    name = models.CharField(max_length=250, blank=True)
    description = models.TextField(max_length=250, blank=False)

    status_choices = [
        (0, "Wait approved"),
        (1, "Approved"),
        (-1, "Rejected"),
        (-2, 'On edit'),
        (-100, 'Dont show')
    ]

    status = models.SmallIntegerField(choices=status_choices, default=0)
