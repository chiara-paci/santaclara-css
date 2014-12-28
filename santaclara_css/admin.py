from django.contrib import admin
from django.utils.html import format_html

from santaclara_css.models import CssColor,CssColorVariable,CssShadow,CssShadowVariable,CssShadowThrough
from santaclara_css.models import CssEquivalence,CssEquivalenceStyle,CssEquivalenceMembership

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


admin.site.register(CssShadowVariable,CssShadowVariableAdmin)

class CssEquivalenceMembershipInline(admin.TabularInline):
    model = CssEquivalenceMembership
    extra = 0

class CssEquivalenceAdmin(admin.ModelAdmin):
    inlines = [ CssEquivalenceMembershipInline ]

admin.site.register(CssEquivalence,CssEquivalenceAdmin)
admin.site.register(CssEquivalenceStyle)
admin.site.register(CssEquivalenceMembership)


