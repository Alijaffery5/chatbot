from django.urls import path
from .views import signup, login, test_token, update_message, delete_chat, chat_operations

urlpatterns = [
    path('register/', signup, name='register_user'),
    path('login/', login, name='login_user'),
    path('test_token/', test_token, name='test_token'),
    path('chats/', chat_operations, name='chat_operations'),
    path('chats/<int:chat_id>/messages/<str:message_id>/', update_message, name='update_message'),
    path('chats/<int:chat_id>/', delete_chat, name='delete_chat'),
]
