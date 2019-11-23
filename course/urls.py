from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # ----- Views for Course Items (Materials)
    # Regular Views deliver full pages
    path('<uuid:course_id>/items', views.CourseItemListView.as_view(), name = 'courseitem_list'),
    path('<uuid:course_id>/create_item', views.CourseItemCreateView.as_view(), name = 'courseitem_create'),
    path('<uuid:course_id>/update_item/<int:item_id>', views.CourseItemUpdateView.as_view(), name = 'courseitem_update'),
    path('<uuid:course_id>/item/<int:item_id>', views.CourseItemDetailView.as_view(), name = 'courseitem_detail'),

    # Inline Views deliver snippets of HTML or sometimes even empty HttpResponses
    path('<uuid:course_id>/create_item_heading_inline', views.CourseItemHeadingCreateInlineView.as_view(), name = 'courseitem_heading_create_inline'),
    path('<uuid:course_id>/update_item_heading_visible_inline', views.CourseItemHeadingVisibleUpdateInlineView.as_view(), name = 'courseitem_heading_visible_update_inline'),
    path('<uuid:course_id>/delete_item_heading_inline', views.CourseItemHeadingDeleteInlineView.as_view(), name = 'courseitem_heading_delete_inline'),
    path('<uuid:course_id>/update_item_order_inline', views.CourseItemOrderUpdateInlineView.as_view(), name = 'courseitem_order_update_inline'),
    path('<uuid:course_id>/update_item_visible_inline', views.CourseItemVisibleUpdateInlineView.as_view(), name = 'courseitem_visible_update_inline'),
    path('<uuid:course_id>/delete_item_inline', views.CourseItemDeleteInlineView.as_view(), name = 'courseitem_delete_inline'),
    path('<uuid:course_id>/delete_item_set_inline', views.CourseItemDeleteSetInlineView.as_view(), name = 'courseitem_delete_set_inline'),

    # ----- Views for Assignements
    path('<uuid:course_id>/assignments', views.AssignmentListView.as_view(), name = 'course_assignment_list'),

    # ----- Views for Attendance
    path('<uuid:course_id>/attendance', views.RollCallListView.as_view(), name = 'rollcall_list'),

    path('<uuid:course_id>/gradebook', views.GradebookView.as_view(), name = 'course_gradebook'),
    path('<uuid:course_id>/settings', views.CourseSettingsView.as_view(), name = 'course_settings'),


    path('preview_markdown', views.MarkdownPreviewView.as_view(), name = 'markdown_preview'),

    path('<uuid:course_id>/', RedirectView.as_view(url = 'items/')),
]
