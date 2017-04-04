
import sys
import hashlib

from io import BytesIO
from PIL import Image, ImageDraw

from django.conf import settings
from django.core.cache import cache
from django.conf.urls import url
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

from django.forms import Form, IntegerField

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import etag

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

    def generate(self, image_format='PNG'):

        height = self.cleaned_data['height']
        width = self.cleaned_data['width']

        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        if content is None:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.draw(image)
            text = '{} X {}'.format(width, height)
            text_width, text_height = draw.textsize(text)
            if text_width < width and text_height < height:
                text_top = (height - text_height) // 2
                text_left = (width - text_width) // 2
                draw.text((text_left, text_top), text, fill=(255, 255, 255))
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60 * 60)
            return content
        return content


def generate_etag(request, width, height):
    content = 'Placeholder: {} X {}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(generate_etag)
def placeholder(request, width, height):

    form = ImageForm({'height': height, 'width': width})

    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
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

