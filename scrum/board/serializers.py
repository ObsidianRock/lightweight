
from datetime import date

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Sprint, Task


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(source='username', read_only=True)
    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        request = self.context['request']
        username = obj.get_username()

        return {
            'self': reverse('user-detail',
                            kwargs={User.USERNAME_FIELD: username},
                            request=request),
            'tasks': '{}?assigned={}'.format(
                reverse('task-list', request=request), username)

        }

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')


class SprintSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('sprint-detail',
                            kwargs={'pk': obj.pk},
                            request=request),
            'tasks': reverse('task-list',
                             request=request) + '?sprint={}'.format(obj.pk),
        }

    def validate_end(self, value):
        new = self.instance is None
        changed = self.instance and self.instance.end != value
        if (new or changed) and (value < date.today()):
            msg = _('End date cannot be in the past.')
            raise serializers.ValidationError(msg)
        return value

    class Meta:
        model = Sprint
        fields = ('id', 'name', 'description', 'end', 'links')


class TaskSerializer(serializers.ModelSerializer):

    status_display = serializers.SerializerMethodField()
    assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,
                                            required=False,
                                            queryset=User.objects.all())
    links = serializers.SerializerMethodField()

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_links(self, obj):
        request = self.context['request']

        links = {
            'self': reverse('task-detail',
                            kwargs={'pk': obj.pk},
                            request=request),
            'sprint': None,
            'assigned': None
        }

        if obj.sprint_id:
            links['sprint'] = reverse('sprint-detail',
                                      kwargs={'pk': obj.sprint_id},
                                      request=request)
        if obj.assigned:
            links['assigned'] = reverse('user-detail',
                                        kwargs={User.USERNAME_FIELD: obj.assigned},
                                        request=request)

        return links

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint', 'status', 'status_display',
                  'order', 'assigned', 'started', 'due', 'completed', 'links')
