from django import template

from midcityapp.models import Volunteership

register = template.Library()


@register.simple_tag(name='is_already_applied')
def is_already_applied(event, user):
    applied = Volunteership.objects.filter(event=event, user=user)
    if applied:
        return True
    else:
        return False
