from django import template

register = template.Library()


@register.filter
def convert_th13_trance(value) -> str:
    # last stage trance is empty string
    if value == "":
        return ""

    try:
        int(value)
    except (ValueError, TypeError):
        return "invalid trance value"

    gauge_units = int(value) // 200
    gauge_progress = int(value) % 200
    return str(gauge_units) + " + " + str(gauge_progress) + "/200"
