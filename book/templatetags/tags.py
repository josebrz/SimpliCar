from django import template

from book.models import Author

register = template.Library()


@register.filter(name='author_count')
def author_count(library):
    return Author.objects.filter(book__libraries__id=library.id).distinct().count()


@register.filter(name='libraries_name')
def libraries_name(libraries):
    return ', '.join([library.name for library in libraries])
