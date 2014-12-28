from santaclara_css.models import CssColorVariable,CssShadowVariable,CssEquivalenceColorVariable

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
    for color_var in CssEquivalenceColorVariable.objects.all():
        name=unicode(color_var.name)
        for eq_color in color_var.equivalence.cssequivalencecolor_set.all():
            style=unicode(eq_color.style).upper()
            T["COLOR_"+style+"_"+name]=color_var.equivalence.color_desc(eq_color.color)
    return T
