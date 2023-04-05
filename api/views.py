from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.serializer import UserSerializer,TaskSerializer
from todos.models import Tasks
from rest_framework import authentication,permissions
class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

class TaskView(ModelViewSet):
    serializer_class=TaskSerializer
    queryset=Tasks.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    http_method_names=["get","post"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self,request,*args,**kwargs):
        qs=Tasks.objects.filter(user=request.user)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)
    
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class TasksdetailsView(GenericViewSet,mixins.DestroyModelMixin):
    serializer_class=TaskSerializer
    queryset=Tasks.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwnerOrReadOnly]

    http_method_names=["delete","put"]

    # def destroy(self, request, *args, **kwargs):
    #     id=kwargs.get("pk")
    #     obj=Tasks.objects.get(id=id)
    #     if obj.user == request.user:
    #         return super().destroy(request,*args,**kwargs)
    #     else:
    #         return Response(data="not able to perform this operation")