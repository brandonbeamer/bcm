from django.shortcuts import reverse
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('overview/', views.OverviewView.as_view(), name = 'overview'),
    path('profile/', views.ProfileView.as_view(), name = 'profile'),
    path('my_courses/', views.MyCoursesView.as_view(), name = 'my_courses'),
    path('create_course/', views.CreateCourseView.as_view(), name = 'create_course'),
    path('find_course/', views.FindCourseView.as_view(), name = 'find_course'),
    path('enroll/<uuid:pk>/', views.EnrollView.as_view(), name = 'enroll'),
    path('account/', views.AccountView.as_view(), name = 'account'),
    path('', RedirectView.as_view(url = 'overview/'))
]
