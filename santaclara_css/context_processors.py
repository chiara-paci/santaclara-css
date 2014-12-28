from santaclara_css.models import CssColorVariable,CssShadowVariable

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

def equivalence_colors(request=None):
    T={}
    for equivalence in CssEquivalenceColorVariable.objects.all():
        name=unicode(equivalence.name)
        for eq_color in equivalence.cssequivalencecolor_set.all():
            style=unicode(eq_color.style).upper()
            T["COLOR_"+style+"_"+name]=equivalence.color_desc(eq_color.color)
    return T
