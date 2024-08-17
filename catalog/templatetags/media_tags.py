from django import template

register = template.Library()

@register.filter(name='media_url')
def media_url(path):
    if path:
        return f'/media/{path}'
    return '#'
