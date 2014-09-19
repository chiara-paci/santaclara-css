from django.contrib import admin
from django.utils.html import format_html

from santaclara_css.models import CssColor,CssColorVariable

class CssColorAdmin(admin.ModelAdmin):
    list_display=[ "hexadecimal","name","color_box","red","green","blue"]
    list_editable=[ "name" ]
    
    def color_box(self,obj):
        return format_html('<span style="background: rgb({0}); width: 3em; height: 1em;">&nbsp;</span>',
                           obj.rgb())

    color_box.allow_tags = True

admin.site.register(CssColor,CssColorAdmin)

class CssColorVariableAdmin(admin.ModelAdmin):
    list_display=[ "name","color_box","alpha","color","rgb"]
    list_editable=["color"]

    def rgb(self, obj):
        return obj.color.rgb()
    rgb.admin_order_field  = 'color'
    rgb.short_description = 'RGB'

    def color_box(self,obj):
        return format_html('<span style="background: {0}; width: 3em; height: 1em;">&nbsp;</span>',
                           obj.color.rgb())
    color_box.allow_tags = True

admin.site.register(CssColorVariable,CssColorVariableAdmin)
