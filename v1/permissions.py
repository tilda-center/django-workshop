from django.contrib.auth.models import User, Group
from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name="student").first())


class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name="professor").first())

