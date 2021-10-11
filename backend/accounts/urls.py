from django.urls import path
from . import views

urlpatterns = [
    path('get-user/', views.GetUserView.as_view(), name="getUser"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
]
