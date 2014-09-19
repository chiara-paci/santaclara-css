from django.contrib import admin

from santaclara_css.models import CssColor,CssColorVariable

class CssColorAdmin(admin.ModelAdmin):
    list_display=[ "name","hexadecimal","red","green","blue"]

admin.site.register(CssColor,CssColorAdmin)

class CssColorVariableAdmin(admin.ModelAdmin):
    list_display=[ "name","alpha","color","rgb"]

    def rgb(self, obj):
        return obj.color.rgb()
    rgb.admin_order_field  = 'color'
    rgb.short_description = 'Color'

admin.site.register(CssColorVariable,CssColorVariableAdmin)
