from django import template
from menu.models import MenuItem
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    root_item = MenuItem.objects.filter(title=menu_name, parent=None).first()
    if root_item:
        root_items = root_item.children.all()
    else:
        root_items = []

    prepared_items = prepare_menu_items(root_items)

    return {'prepared_items': prepared_items, 'request': context['request']}


def prepare_menu_items(items):
    result = []
    for item in items:
        url = resolve_url(item.url)
        result.append({
            'title': item.title,
            'url': url,
            'children': prepare_menu_items(list(item.children.all()))
        })
    return result


def resolve_url(url_value):
    if url_value.startswith('/'):
        return url_value
    else:
        try:
            return reverse(url_value)
        except NoReverseMatch:
            return '#'
