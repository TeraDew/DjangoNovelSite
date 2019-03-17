from django import template
from novel.models import History
register = template.Library()


@register.simple_tag(takes_context=True)
def get_recent_history(context, num=5):
    request = context['request']
    return History.objects.filter(user=request.user).order_by('-read_time')[:num]

