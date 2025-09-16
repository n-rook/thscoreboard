from django import template

register = template.Library()


@register.filter
def convert_th13_trance(value) -> str:
    # last stage trance is empty string
    if value == "":
        return ""

    try:
        gauge_units = int(value) // 200
        gauge_progress = int(value) % 200
        return str(gauge_units) + " + " + str(gauge_progress) + "/200"
    except:
        return "invalid trance value"
