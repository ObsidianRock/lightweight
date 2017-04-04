
import sys


from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

from django.forms import Form, IntegerField

from django.http import HttpResponse, HttpResponseBadRequest

settings.configure(
    DEBUG=True,
    SECRET_KEY='+1iu9s2u*d26zrdo(9xh4&%3!@^+-@(-j+j5^&y61^0_dr-n+1',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)


class ImageForm(Form):

    height = IntegerField(min_value=1, max_value=2000)
    width = IntegerField(min_value=1, max_value=2000)


def placeholder(request, width, height):

    form = ImageForm({'height': height, 'width': width})

    if form.is_valid():
        height = form.cleaned_data['height']
        width = form.cleaned_data['width']

        return HttpResponse('OK')
    else:
        return HttpResponseBadRequest('Invalid image request')


def index(request):
    return HttpResponse('Hello World')


urlpatterns = (
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$',
        placeholder,
        name='placeholder'),
    url(r'^$', index, name='homepage'),
)

application = get_wsgi_application()


if __name__ == "__main__":

    execute_from_command_line(sys.argv)

