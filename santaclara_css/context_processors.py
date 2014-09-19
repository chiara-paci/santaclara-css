from santaclara_css.models import CssColorVariable

def colors(request=None):
    T={}
    for color in CssColorVariable.objects.all():
        T["COLOR_"+unicode(color.name)]=unicode(color)
    return T

def shadows(request=None):
    T={}
    for shadow in CssShadowVariable.objects.all():
        T["SHADOW_"+unicode(shadow.name)]=unicode(shadow)
    return T
