
import sys

from django.conf import settings
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application


from django.http import HttpResponse

settings.configure(
    DEBUG=True,
    SECRET_KEY='SomeSecretKey',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)


def index(request):
    return HttpResponse('Hello Friend')


urlpatterns = (
    url(r'^$', index),
)

application = get_wsgi_application()


if __name__ == "__main__":

    execute_from_command_line(sys.argv)

