from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.TodoListView.as_view(), name="todos"),
    path('todo/<str:id>/', views.TodoDetailView.as_view(), name="todo"),
]
