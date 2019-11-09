from django.urls import path
from django.contrib.auth.views import logout_then_login
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.Login.as_view(), name = 'login'),
    path('logout/', logout_then_login, name = 'logout'),
    path('signup/', views.Signup.as_view(), name = 'signup'),
    path('verify/<str:code>', views.verify, name = 'verify')
]
