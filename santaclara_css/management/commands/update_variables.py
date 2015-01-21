#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,time,datetime,sys

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from santaclara_css.models import CssColorVariable,CssShadowVariable,CssEquivalenceColorVariable,CssEquivalenceShadowVariable,CssVariable

def mk_variable(key,value):
    var_obj,created=CssVariable.objects.get_or_create(key=key,
                                                      defaults={"value":value})
    if created:
        print "Created",key,value
    else:
        var_obj.value=value
        var_obj.save()
        print "Updated",key,value

class Command(BaseCommand):
    help = 'Update css variables'

    def handle(self, *args, **options):

        for color in CssColorVariable.objects.all():
            key="COLOR_"+unicode(color.name)
            value=unicode(color)
            mk_variable(key,value)

        for shadow in CssShadowVariable.objects.all():
            key="SHADOW_"+unicode(shadow.name)
            value=unicode(shadow)
            mk_variable(key,value)

        for color_var in CssEquivalenceColorVariable.objects.all():
            name=unicode(color_var.name)
            for style,color in color_var.color_dict():
                key="COLOR_"+style.upper()+"_"+name
                value=color
                mk_variable(key,value)

        for shadow_var in CssEquivalenceShadowVariable.objects.all():
            name=unicode(shadow_var.name)
            for style,shadow in shadow_var.shadow_dict():
                key="SHADOW_"+style.upper()+"_"+name
                value=shadow
                mk_variable(key,value)
