
import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template
from django.utils._os import safe_join


def get_page_or_404(name):

    try:
        file_path = safe_join(settings.SITE_PAGEs_DIRECTORY, name)
    except ValueError:
        raise Http404('page not found')
    else:
        if not os.path.exists(file_path):
            raise Http404('page not found')

    with open(file_path, 'r') as f:
        template_page = Template(f.read())

    return template_page


def page(request, slug='index'):

    file_name = '{}.html'.format(slug)
    template_page = get_page_or_404(file_name)

    context = {
        'slug': slug,
        'page': template_page
    }

    return render(request, 'page.html', context)
