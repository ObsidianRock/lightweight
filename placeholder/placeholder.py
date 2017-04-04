
import sys

from io import BytesIO
from PIL import Image, ImageDraw

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


    def generate(self, image_format='PNG'):

        height = self.cleaned_data['height']
        width = self.cleaned_data['width']

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
        return content


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

