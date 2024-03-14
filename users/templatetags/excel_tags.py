from django import template

register = template.Library()


@register.filter(name="treat_as_string")
def treat_as_string(value):
    # Convert value to string to ensure proper indexing
    value_str = str(value)
    # Check if the third character of the string is 'E'
    if len(value_str) >= 3 and value_str[2] == "E":
        return f"'{value_str}'"
    return value
