from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('<uuid:pk>/items', views.CourseItemsView.as_view(), name = 'course_items'),
    path('<uuid:pk>/create_item', views.CreateCourseItemView.as_view(), name = 'create_courseitem'),
    path('<uuid:pk>/edit_item/<int:item_id>', views.EditCourseItemView.as_view(), name = 'edit_courseitem'),
    path('<uuid:pk>/view_item/<int:item_id>', views.CourseItemView.as_view(), name = 'view_courseitem'),
    path('<uuid:pk>/assignments', views.AssignmentsView.as_view(), name = 'course_assignments'),
    path('<uuid:pk>/gradebook', views.GradebookView.as_view(), name = 'course_gradebook'),
    path('<uuid:pk>/settings', views.CourseSettingsView.as_view(), name = 'course_settings'),
    path('<uuid:pk>/', RedirectView.as_view(url = 'items/')),
]
