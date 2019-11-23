from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from course.models import ItemCategory, CourseItem

from .serializers import ItemCategorySerializer, CourseItemSerializer
from .permissions import IsEnrolled, InstructorWriteEnrolledRead

# Create your views here.
class CourseItemList(APIView):
    permission_classes = [IsAuthenticated,IsEnrolled]
    def get(self, request, **kwargs):
        items = CourseItem.objects.filter(course = kwargs['course_id'])
        serializer = CourseItemSerializer(items, many=True)
        return Response(serializer.data)

class CourseItemDetail(UpdateModelMixin, APIView):
    permission_classes = [IsAuthenticated, InstructorWriteEnrolledRead]
    def get_object(self, **kwargs):
        return get_object_or_404(CourseItem, course = kwargs['course_id'], id = kwargs['item_id'])

    def get(self, request, **kwargs):
        item = self.get_object(**kwargs)
        serializer = CourseItemSerializer(item)
        return Response(serializer.data)

    def patch(self, request, **kwargs):
        item = self.get_object(**kwargs)

        serializer = CourseItemSerializer(item, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        item = self.get_object(**kwargs)
        item.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
