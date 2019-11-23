from rest_framework import serializers
from course.models import CourseItem, ItemCategory

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['type', 'name', 'order']

class CourseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseItem
        fields = ['id', 'name', 'description', 'content_type', 'category', 'order', 'visible']
