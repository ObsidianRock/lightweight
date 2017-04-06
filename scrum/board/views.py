from django.contrib.auth import get_user_model

from rest_framework import viewsets, authentication, permissions
from .models import Sprint, Task

from .serializers import SprintSerializer, TaskSerializer, UserSerializer

User = get_user_model()


class DefaultMixin:

    authentication_class = (
        authentication.BaseAuthentication,
        authentication.TokenAuthentication,
    )
    permissions_classes = (
        permissions.IsAuthenticated
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class SprintViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer


class TaskViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserViewSets(DefaultMixin, viewsets.ModelViewSet):

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD

    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer