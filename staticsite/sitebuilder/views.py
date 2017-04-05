
import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template
from django.utils._os import safe_join


def get_page_or_404(name):

    try:
        file_path = os.path.join('C:/Users/abdirahman/projects/django_project/lightweight/staticsite/sitebuilder/pages', name)
        print(file_path)
    except ValueError:
        raise Http404('page not found 1st')
    else:
        if not os.path.exists(file_path):
            raise Http404('page not found 2nd')

    with open(file_path, 'r') as f:
        template_page = Template(f.read())

    return template_page


def page(request, slug='index'):

    file_name = '{}.html'.format(slug)
    page = get_page_or_404(file_name)
    context = {
        'slug': slug,
        'page': page,
    }

    return render(request, 'page.html', context)
