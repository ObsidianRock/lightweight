
from django.contrib.auth import get_user_model

import django_filters

from .models import Task

User = get_user_model()


class NullFilter(django_filters.BooleanFilter):

    def filter(self, qs, value):

        if value is not None:
            return qs.filter(**{'%s__isnull' % self.name: value})
        return qs


class TaskFilter(django_filters.FilterSet):

    backlog = NullFilter(name='sprint')

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.filters['assigned'.extra.update(
            {'to_field_name': User.USERNAME_FIELD}
        )


    class Meta:
        model = Task
        fields = ('sprint', 'status', 'assigned', 'backlog')


