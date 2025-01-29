from django.urls import path
from api import views

urlpatterns = [
    path('todo/create/', views.TodoListCreateView.as_view()),
    path('todo/add/', views.TodoCreateView.as_view()),

    # urls.py
    path('todo/user/', views.UserTodosView.as_view(), name='user-todos'),
    path('todo/<int:pk>/', views.TodoUpdateView.as_view(), name='update-todo'),

    path('todo/get/', views.TodoListCreateView.as_view()),

    path('user/create/', views.UserCreateView.as_view()),

    path('user/login/', views.CustomLoginView.as_view()),



    path('handle_query/', views.HandleQueryView.as_view()),
    path('conversations/<int:conversation_id>/', views.ConversationDetailView.as_view(), name='conversation-detail'),

    path('conversations/', views.UserConversationsView.as_view(), name='user-conversations'),

    path('ollama/conversations/<int:conversation_id>/', views.OllamaProcessView.as_view(), name='ollama-process'),

    path('calendar/events/', views.CalendarView.as_view(), name='calendar-events'),

]