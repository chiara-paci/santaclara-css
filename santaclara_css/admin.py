from django.contrib import admin

from santaclara_css.models import CssColor

class CssColorAdmin(admin.ModelAdmin):
    list_display=[ "name","__unicode__","hexadecimal","alpha","red","green","blue"]

admin.site.register(CssColor,CssColorAdmin)
