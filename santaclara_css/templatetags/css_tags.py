from django import template

register = template.Library()

#background: -webkit-gradient(linear, 0% 0%, 0% 100%, from({{ COLOR_H1_BACK_STOP }}), to({{ COLOR_H1_BACK_START }})); 
#background: -webkit-linear-gradient(top, {{ COLOR_H1_BACK_START }}, {{ COLOR_H1_BACK_STOP }}); 
#background: -moz-linear-gradient(top, {{ COLOR_H1_BACK_START }}, {{ COLOR_H1_BACK_STOP }}); 
#background: -ms-linear-gradient(top, {{ COLOR_H1_BACK_START }}, {{ COLOR_H1_BACK_STOP }}); 
#background: -o-linear-gradient(top, {{ COLOR_H1_BACK_START }}, {{ COLOR_H1_BACK_STOP }}); 

@register.simple_tag
def columned(num):
    S='-moz-column-count:'+str(num)+';\n'
    S+='-webkit-column-count:'+str(num)+';\n'
    S+='column-count:'+str(num)+';'
    return S


#def background_gradient(style,start,stop):
#    gradient='linear-gradient('+style+','+start+','+stop+')'
@register.simple_tag
def background_gradient(style,*args):
    colors=",".join(args);
    gradient='linear-gradient('+style+','+colors+')'
    S='background: '+gradient+';\n'
    # inverso rispetto agli altri, questo per style=top, cambiare se serve altro
    #S+='background: -webkit-gradient(linear, 0% 0%, 0% 100%, from('+stop+'), to('+start+'));'
    for i in ["webkit","moz","ms","o"]:
        S+='background: -'+i+'-'+gradient+';\n'
    return S

@register.simple_tag
def border_radius(radius):
    S='border-radius: '+radius+';'
    for i in ["webkit","moz"]:
        S+='\n-'+i+'-border-radius: '+radius+';'
    return S

@register.simple_tag
def box_shadow(shadow):
    S='box-shadow: '+shadow+';'
    for i in ["webkit","moz"]:
        S+='\n-'+i+'-box-shadow: '+shadow+';'
    return S

@register.simple_tag
def border_radius_pos(pos,radius):
    S=''
    if pos in ["top","left","top-left"]:
        S+='border-top-left-radius: '+radius+';\n'
        S+='-moz-border-radius-topleft: '+radius+';\n'
        S+='-webkit-bordertop-left-radius: '+radius+';\n'
    if pos in ["top","right","top-right"]:
        S+='border-top-right-radius: '+radius+';\n'
        S+='-moz-border-radius-topright: '+radius+';\n'
        S+='-webkit-bordertop-right-radius: '+radius+';\n'
    if pos in ["bottom","left","bottom-left"]:
        S+='border-bottom-left-radius: '+radius+';\n'
        S+='-moz-border-radius-bottomleft: '+radius+';\n'
        S+='-webkit-borderbottom-left-radius: '+radius+';\n'
    if pos in ["bottom","right","bottom-right"]:
        S+='border-bottom-right-radius: '+radius+';\n'
        S+='-moz-border-radius-bottomright: '+radius+';\n'
        S+='-webkit-borderbottom-right-radius: '+radius+';\n'
    return S

@register.simple_tag
def text_rotation(degree):
    S='transform: rotate('+degree+'deg);'
    for i in ["webkit","ms"]:
        S+='\n-'+i+'-transform: rotate('+degree+'deg);'
    return S

@register.simple_tag
def icon_file_manager_levels(levels,step):
    levels=int(levels)
    step=float(step)
    S=""
    S+=", ".join(map(lambda x: ".iconlevel"+unicode(x),range(0,levels)))
    S+=" {\n"
    S+="vertical-align: bottom;\n"
    S+="font-size: 1.1em;\n"
    S+="}\n\n"
    for n in range(1,levels):
        S+=".iconlevel"+unicode(n)+" {\n"
        S+="padding-left: %2.2fem;\n" % (n*step)
        S+="}\n\n"
    return S



