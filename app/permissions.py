
from rest_framework import permissions
from rest_framework.permissions import BasePermission

from .models import *

class IsAllUser(BasePermission):
    """
    Allows access to Artist user, Professional user and Institution.
    """
    def has_permission(self, request, view):
        return request.user and request.user.id and \
                    request.user.is_authenticated and \
                    (request.user.user_type == 'Artist' or \
                    request.user.user_type == 'Professional' or \
                    request.user.user_type == 'Institution')


class IsArtistUser(BasePermission):
    """
    Allows access only to authenticated and Artist users.
    """
    message = 'Only Artist user allowed.'
    def has_permission(self, request, view,*args, **kwargs):
        try:
            user = MyUser.objects.get(id=request.user.id,user_type = 'Artist')
            return request.user and request.user.is_authenticated
        except:
            return None

class IsProfessionalUser(BasePermission):
    """
    Allows access only to authenticated and Professional users.
    """
    message = 'Only Professional user allowed.'
    def has_permission(self, request, view,*args, **kwargs):
        try:
            user = MyUser.objects.get(id=request.user.id,user_type = 'Professional')
            return request.user and request.user.is_authenticated
        except:
            return None


class IsInstitutionUser(BasePermission):
    """
    Allows access only to authenticated and Institution users.
    """
    message = 'Only Institution user allowed.'
    def has_permission(self, request, view,*args, **kwargs):
        try:
            user = MyUser.objects.get(id=request.user.id,user_type = 'Institution')
            return request.user and request.user.is_authenticated
        except:
            return None

