from django.shortcuts import render

from rest_framework import viewsets, authentication, permissions
from .models import Sprint
from .serializers import SprintSerializer


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

    queryset = Sprint.Object.order_by('end')
    serializer_class = SprintSerializer


