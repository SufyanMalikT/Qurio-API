from rest_framework.permissions import BasePermission
class CustomUserPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT','PATCH','DELETE']:
            if request.user.is_authenticated:
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username or request.user.is_superuser
        
class QuestionPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST','PUT','PATCH','DELETE']:
            return request.user.is_authenticated
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            return obj.author.username == request.user.username or request.user.is_superuser
        return True
    
class AnswerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST','PUT','PATCH','DELETE']:
            return request.user.is_authenticated
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            return obj.author.username == request.user.username or request.user.is_superuser
        return True
    
class TagsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST','PUT','PATCH','DELETE']:
            return request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser  