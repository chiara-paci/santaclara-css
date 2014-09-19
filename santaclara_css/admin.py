from django.contrib import admin

from santaclara_css.models import CssColor,CssColorVariable

class CssColorAdmin(admin.ModelAdmin):
    list_display=[ "name","hexadecimal","red","green","blue"]

admin.site.register(CssColor,CssColorAdmin)

class CssColorVariableAdmin(admin.ModelAdmin):
    list_display=[ "name","alpha","color_name","color"]

    def color_name(self, obj):
        return obj.color.name
    get_name.admin_order_field  = 'color'
    get_name.short_description = 'Color Name'

admin.site.register(CssColorVariable,CssColorVariableAdmin)
