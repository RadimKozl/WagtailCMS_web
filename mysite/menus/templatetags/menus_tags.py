from django import template
from .. models import Menu

register = template.Library()

@register.simple_tag()
def get_menu(slug):
    """Get a menu by its slug."""
    return Menu.objects.get(slug=slug)
