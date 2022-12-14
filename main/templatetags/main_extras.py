from django import template

register = template.Library()

@register.filter
def add_or_replace_q(value, arg):
    if (arg + '=') in value:
        arr = str(value).replace("/?", "").split('&')
        for i in range(len(arr)):
            if (arg + '=') in arr[i]:
                arr.pop(i)
                break
        value = "/?" + "&".join(arr) + "&"
    elif "?" not in value:
        value = "/?"
    else:
        value += "&"
    return value
