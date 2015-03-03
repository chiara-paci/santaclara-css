from django.contrib import admin
from django.utils.html import format_html

from santaclara_css.models import CssColor,CssColorVariable,CssShadow,CssShadowVariable,CssShadowThrough
from santaclara_css.models import CssEquivalence,CssEquivalenceStyle,CssEquivalenceColor,CssEquivalenceColorVariable
from santaclara_css.models import CssEquivalenceShadowVariable,CssEquivalenceShadowThrough,CssVariable

from santaclara_css.models import CssEquivalenceBorder
from santaclara_css.models import CssEquivalenceLinearGradient
from santaclara_css.models import CssEquivalenceLinearGradientThrough
from santaclara_css.models import CssEquivalenceSelector
from santaclara_css.models import CssEquivalenceStanza
from santaclara_css.models import CssEquivalenceStanzaBoxShadowThrough
from santaclara_css.models import CssEquivalenceStanzaBorderThrough
from santaclara_css.models import CssEquivalenceStanzaColorThrough
from santaclara_css.models import CssEquivalenceStanzaLinearGradientThrough

class CssVariableAdmin(admin.ModelAdmin):
    list_display=[ "key","value"]

admin.site.register(CssVariable,CssVariableAdmin)

class CssColorAdmin(admin.ModelAdmin):
    list_display=[ "hexadecimal","name","color_box","red","green","blue"]
    list_editable=[ "name" ]
    
    def color_box(self,obj):
        return format_html('<span style="background: rgb({0}); width: 30em; height: 1em;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>',
                           obj.rgb())

    color_box.allow_tags = True

admin.site.register(CssColor,CssColorAdmin)

class CssColorVariableAdmin(admin.ModelAdmin):
    list_display=[ "name","color_box","alpha","color","rgb"]
    list_editable=["color","alpha"]
    save_as=True

    def rgb(self, obj):
        return obj.color.rgb()
    rgb.admin_order_field  = 'color'
    rgb.short_description = 'RGB'

    def color_box(self,obj):
        return format_html('<span style="background: {0}; width: 3em; height: 1em;">&nbsp;</span>',
                           obj.color.rgb())
    color_box.allow_tags = True

admin.site.register(CssColorVariable,CssColorVariableAdmin)

class CssShadowAdmin(admin.ModelAdmin):
    list_display=[ "__unicode__","h_shadow","v_shadow","blur","spread"]
    list_editable=[ "h_shadow","v_shadow","blur","spread"]
    

admin.site.register(CssShadow,CssShadowAdmin)

class CssShadowThroughInline(admin.TabularInline):
    model = CssShadowThrough
    extra = 0

class CssShadowVariableAdmin(admin.ModelAdmin):
    list_display=[ "name", "__unicode__" ]
    inlines = [ CssShadowThroughInline ]
    save_as=True

admin.site.register(CssShadowVariable,CssShadowVariableAdmin)

class CssEquivalenceColorInline(admin.TabularInline):
    model = CssEquivalenceColor
    extra = 0

class CssEquivalenceAdmin(admin.ModelAdmin):
    inlines = [ CssEquivalenceColorInline ]

admin.site.register(CssEquivalence,CssEquivalenceAdmin)

class CssEquivalenceStyleAdmin(admin.ModelAdmin):
    inlines = [ CssEquivalenceColorInline ]

admin.site.register(CssEquivalenceStyle,CssEquivalenceStyleAdmin)
admin.site.register(CssEquivalenceColor)

class CssEquivalenceColorVariableAdmin(admin.ModelAdmin):
    list_display=[ "name","color_box","alpha","equivalence","rgb"]
    list_editable=["equivalence","alpha"]
    save_as=True

    def rgb(self, obj):
        T=[]
        for eq_color in obj.equivalence.cssequivalencecolor_set.all():
            T.append(eq_color.color.rgb())
        return "/".join(T)
    rgb.short_description = 'RGB'

    def color_box(self,obj):
        T=[]
        for eq_color in obj.equivalence.cssequivalencecolor_set.all():
            T.append('<span style="background: #%s; width: 3em; height: 1em;">%s</span>' % (eq_color.color.hexadecimal,
                                                                                           unicode(eq_color.style)) )
        return format_html(" ".join(T))
    color_box.allow_tags = True

admin.site.register(CssEquivalenceColorVariable,CssEquivalenceColorVariableAdmin)

class CssEquivalenceShadowThroughInline(admin.TabularInline):
    model = CssEquivalenceShadowThrough
    extra = 0

class CssEquivalenceShadowVariableAdmin(admin.ModelAdmin):
    list_display=[ "name", "__unicode__" ]
    inlines = [ CssEquivalenceShadowThroughInline ]
    save_as=True

admin.site.register(CssEquivalenceShadowVariable,CssEquivalenceShadowVariableAdmin)


#####

admin.site.register(CssEquivalenceBorder)
admin.site.register(CssEquivalenceLinearGradient)
admin.site.register(CssEquivalenceLinearGradientThrough)
admin.site.register(CssEquivalenceSelector)
admin.site.register(CssEquivalenceStanzaBoxShadowThrough)
admin.site.register(CssEquivalenceStanzaBorderThrough)
admin.site.register(CssEquivalenceStanzaColorThrough)
admin.site.register(CssEquivalenceStanzaLinearGradientThrough)

class CssEquivalenceStanzaBoxShadowThroughInline(admin.TabularInline):
    model = CssEquivalenceStanzaBoxShadowThrough
    extra = 0

class CssEquivalenceStanzaBorderThroughInline(admin.TabularInline):
    model = CssEquivalenceStanzaBorderThrough
    extra = 0

class CssEquivalenceStanzaLinearGradientThroughInline(admin.TabularInline):
    model = CssEquivalenceStanzaLinearGradientThrough
    extra = 0

class CssEquivalenceStanzaColorThroughInline(admin.TabularInline):
    model = CssEquivalenceStanzaColorThrough
    extra = 0

class CssEquivalenceStanzaAdmin(admin.ModelAdmin):
    inlines = [ CssEquivalenceStanzaBoxShadowThroughInline,
                CssEquivalenceStanzaBorderThroughInline,
                CssEquivalenceStanzaLinearGradientThroughInline,
                CssEquivalenceStanzaColorThroughInline]

admin.site.register(CssEquivalenceStanza,CssEquivalenceStanzaAdmin)

