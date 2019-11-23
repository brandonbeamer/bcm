from django.urls import path
from . import views

urlpatterns = [
    path('item_list/<uuid:course_id>/', views.CourseItemList.as_view(), name = "api_item_list"),
    path('item_detail/<uuid:course_id>/<int:item_id>/', views.CourseItemDetail.as_view(), name = "api_item_detail"),
]
