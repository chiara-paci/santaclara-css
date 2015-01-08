from santaclara_css.models import CssColorVariable,CssShadowVariable,CssEquivalenceColorVariable,CssEquivalenceShadowVariable

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
        for style,color in color_var.color_dict():
            T["COLOR_"+style.upper()+"_"+name]=color
    return T

def equivalence_shadows(request=None):
    T={}
    for shadow_var in CssEquivalenceShadowVariable.objects.all():
        name=unicode(shadow_var.name)
        for style,shadow in shadow_var.shadow_dict():
            T["SHADOW_"+style.upper()+"_"+name]=shadow
    return T
