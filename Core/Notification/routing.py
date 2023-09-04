
from channels.routing import URLRouter
from django.urls import path


from .consumer import NotificationConsumer

websockets_url = URLRouter([
    path("ws/Notification/", NotificationConsumer.as_asgi()),

])


