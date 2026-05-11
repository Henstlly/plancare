from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать объект только его владельцу.
    Остальные могут только читать.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsCatOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать/создавать вакцинации только владельцу кота.
    Остальные могут только читать.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.cat.owner == request.user
