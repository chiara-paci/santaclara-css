from santaclara_css.models import CssColorVariable

def colors(request=None):
    T={}
    for color in CssColorVariable.objects.all():
        T["COLOR_"+unicode(color.name)]=unicode(color)
    return T
