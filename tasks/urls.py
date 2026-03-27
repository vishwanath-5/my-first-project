from django.urls import path
from .views import TaskListCreateView, TaskDetailView
urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
from .views import register, login
urlpatterns += [
    path('register/', register),
    path('login/', login),
]