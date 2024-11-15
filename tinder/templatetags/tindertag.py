from django import template


register = template.Library()

@register.filter(name="get_item")
def get_item(dict_obj: dict, index: str):
    try:
        return dict_obj[str(index)]
    except (IndexError, ValueError, TypeError):
        return None