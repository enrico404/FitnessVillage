from django import template

register = template.Library()


@register.filter(name='get_at_index')
def get_at_index(list, index):
    return list[index]

@register.filter(name='has_group')
def has_group(user, groupName):
    return user.groups.filter(name=groupName).exists()