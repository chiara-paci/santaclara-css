from django.contrib import admin

from santaclara_css.models import CssColor,CssColorVariable

class CssColorAdmin(admin.ModelAdmin):
    list_display=[ "hexadecimal","name","red","green","blue"]
    list_editable=[ "name" ]

admin.site.register(CssColor,CssColorAdmin)

class CssColorVariableAdmin(admin.ModelAdmin):
    list_display=[ "name","alpha","color","rgb"]
    list_editable=["color"]

    def rgb(self, obj):
        return obj.color.rgb()
    rgb.admin_order_field  = 'color'
    rgb.short_description = 'RGB'

admin.site.register(CssColorVariable,CssColorVariableAdmin)
