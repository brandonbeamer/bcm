from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('<uuid:course_id>/items', views.CourseItemListView.as_view(), name = 'course_item_list'),
    path('<uuid:course_id>/create_item_heading_inline', views.ItemHeadingCreateInlineView.as_view(), name = 'course_item_list_heading_create_inline'),
    path('<uuid:course_id>/create_item', views.CourseItemCreateView.as_view(), name = 'course_item_create'),
    path('<uuid:course_id>/update_item/<int:item_id>', views.CourseItemUpdateView.as_view(), name = 'course_item_update'),
    path('<uuid:course_id>/item/<int:item_id>', views.CourseItemDetailView.as_view(), name = 'course_item_detail'),
    path('<uuid:course_id>/assignments', views.AssignmentListView.as_view(), name = 'course_assignment_list'),
    path('<uuid:course_id>/gradebook', views.GradebookView.as_view(), name = 'course_gradebook'),
    path('<uuid:course_id>/settings', views.CourseSettingsView.as_view(), name = 'course_settings'),
    path('<uuid:course_id>/', RedirectView.as_view(url = 'items/')),
]
