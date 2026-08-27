from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def querystring(context, **params):
    """نسخة متوافقة من وسم {% querystring %} المدمج في جانغو 5.1+."""
    request = context['request']
    query = request.GET.copy()
    for key, value in params.items():
        if value in (None, ''):
            query.pop(key, None)
        else:
            query[key] = value
    encoded = query.urlencode()
    return f'?{encoded}' if encoded else ''


@register.filter
def is_active_url(path, base):
    """True إذا كانت الصفحة الحالية هي عنصر القائمة أو صفحة فرعية تابعة له."""
    base = base or ''
    path = path or ''
    if path == base:
        return True
    return base.endswith('/') and path.startswith(base)
