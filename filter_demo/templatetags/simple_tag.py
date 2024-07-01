from django import template

register = template.Library()

@register.simple_tag
def greet_user(message, username):
    return "{greet_message}, {user}!!!".format(greet_message=message, user=username)