from rest_framework import permissions
from course.views import verify_enrollment, verify_instructor

class IsEnrolled(permissions.BasePermission):
    def has_permission(self, request, view):
        return verify_enrollment(view, update_context = False)

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return verify_instructor(view, update_context = False)

class InstructorWriteEnrolledRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return verify_enrollment(view, update_context = False)

        return verify_instructor(view, update_context = False)
