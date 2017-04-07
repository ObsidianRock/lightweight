from django.contrib.auth import get_user_model

from rest_framework import viewsets, authentication, permissions, filters

from .models import Sprint, Task

from .serializers import SprintSerializer, TaskSerializer, UserSerializer

from .forms import TaskFilter, SprintFilter

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
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )


class SprintViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    filter_class = SprintFilter
    search_fields = ('name', )
    ordering_fields = ('end', 'name',)


class TaskViewSet(DefaultMixin, viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    search_fields = ('name', 'description',)
    ordering_fields = ('name', 'order', 'started', 'due', 'completed',)
    filter_class = TaskFilter


class UserViewSets(DefaultMixin, viewsets.ModelViewSet):

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD

    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer

    search_fields = (User.USERNAME_FIELD,)