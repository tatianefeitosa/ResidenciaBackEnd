from rest_framework import permissions

class IsAdministrador(permissions.BasePermission):
    """Permite acesso apenas a usuários administradores."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'administrador'


class IsSolicitante(permissions.BasePermission):
    """Permite acesso apenas a usuários solicitantes."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'solicitante'
