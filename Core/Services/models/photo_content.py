from django.db import models
from django_fsm import FSMIntegerField, transition


class PhotoStateEnum:
    WAIT_APPROVED = 0  # В ожидании публикации
    APPROVED = 1  # Опубликовано
    REJECTED = -1  # На удалении
    ON_EDIT = -2  # Редактируется
    DONT_SHOW = -100  # Отклонено/удалено


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

    state = FSMIntegerField(default=PhotoStateEnum.WAIT_APPROVED)

    @transition(state, source=PhotoStateEnum.WAIT_APPROVED, target=PhotoStateEnum.APPROVED)
    def publish(self):
        self.state = PhotoStateEnum.APPROVED
        self.save()

    @transition(state, source=PhotoStateEnum.WAIT_APPROVED, target=PhotoStateEnum.REJECTED)
    def rejected(self):
        self.state = PhotoStateEnum.REJECTED
        self.save()

    @transition(state, source=PhotoStateEnum.APPROVED, target=PhotoStateEnum.ON_EDIT)
    def start_edit(self):
        self.state = PhotoStateEnum.ON_EDIT
        self.save()

    @transition(state, source=PhotoStateEnum.ON_EDIT, target=PhotoStateEnum.APPROVED)
    def edit_success(self):
        self.state = PhotoStateEnum.APPROVED
        self.save()

    @transition(state, source=PhotoStateEnum.ON_EDIT, target=PhotoStateEnum.DONT_SHOW)
    def fail_edit(self):
        self.state = PhotoStateEnum.DONT_SHOW
        self.save()

    @transition(state, source=PhotoStateEnum.APPROVED, target=PhotoStateEnum.REJECTED)
    def initial_delete(self):
        self.state = PhotoStateEnum.REJECTED
        self.save()

    @transition(state, source=PhotoStateEnum.REJECTED, target=PhotoStateEnum.DONT_SHOW)
    def finish_delete(self):
        self.state = PhotoStateEnum.DONT_SHOW
        self.save()

    @transition(state, source=PhotoStateEnum.REJECTED, target=PhotoStateEnum.APPROVED)
    def cancel_delete(self):
        self.state = PhotoStateEnum.APPROVED
        self.save()
