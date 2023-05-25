from django import template

register = template.Library()

@register.filter
def slice_queryset(queryset, num):
    return queryset[:num]
 

@register.filter
def comment_by_time(queryset):
    return queryset.order_by('-blog_comment_time')
