from rest_framework.permissions import BasePermission
from .models import User, ServiceRequest

class IsPIN(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_PIN

class IsCV(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_CV

class IsCSR(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_CSR

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_ADMIN

class CanEditPendingRequest(BasePermission):
    # PIN can edit/delete only if status is PENDING
    def has_object_permission(self, request, view, obj: ServiceRequest):
        return obj.pin == request.user and obj.status == ServiceRequest.STATUS_PENDING