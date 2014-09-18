
from santaclara_css.models import CssColor

def colors(request=None):
    T={}
    for color in CssColor.objects.all():
        T["COLOR_"+unicode(color.name)]=unicode(color)
    return T
