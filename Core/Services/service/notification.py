from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def like_notification(like_id, action, user_id, work_username, like_count):
    channel_layers = get_channel_layer()

    event = {
        'type': 'send_notification_event',
        'user_photo_id': user_id.id,
    }
    if action == "CreatedLike":
        event.update({'notification': "Был поставлен лайк к вашему фото " + like_id + " Пользователем " +
                                      work_username + "\n" + "На данный момент количество лайков:" + like_count})
    if action == "DeletedLike":
        event.update({'notification': 'Был убран лайк с вашего фото ' + like_id + " Пользователем " + work_username +
                                      "\n На данный момент количество лайков:" + like_count})
    async_to_sync(channel_layers.group_send)('notification', event)


def comment_notification(photo_id, user_id, action, work_username, comments_count):
    channel_layers = get_channel_layer()
    event = {
        'type': 'send_notification_event',
        'user_photo_id': user_id.id,
    }
    if action == "CreatedComment":
        event.update({'notification': 'Был оставлен комментарий к вашему фото ' + photo_id + "Пользователем " +
                                      work_username + "\n" + "На данный момент количество комментариев: " +
                                      comments_count})

    if action == "DeletedComment":
        event.update({'notification': 'Был удален комментарий с вашего фото ' + photo_id + "Пользователем " +
                                      work_username + "\n" + "На данный момент количество комментариев: " +
                                      comments_count})
    async_to_sync(channel_layers.group_send)('notification', event)


def global_notification(text):
    channel_layers = get_channel_layer()
    event = {
        'type': 'send_global_event',
        'notification': text
    }
    async_to_sync(channel_layers.group_send)('notification', event)
