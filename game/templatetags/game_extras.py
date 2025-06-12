from django import template
register = template.Library()

@register.filter
def index(seq, i):
    return seq[i]

