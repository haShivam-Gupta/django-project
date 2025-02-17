from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_ui, name='chatbot_ui'),
    path('handle_chat/', views.handle_chat, name='handle_chat'),
    path('reset-session/', views.reset_session, name='reset_session'),
]
