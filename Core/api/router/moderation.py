from django.urls import path
from ..views.moderation import *

urlpatterns = [
    path('publication/', PublishView.as_view()),
    path('reject/', RejectView.as_view()),
    path('changes/', ChangeView.as_view()),

]
