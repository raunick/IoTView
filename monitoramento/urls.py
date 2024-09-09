from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.get_messages, name='get_messages'),
    path('action_messages/', views.get_action_messages, name='get_action_messages'),
    path('publish/', views.publish_message, name='publish_message'),
]
