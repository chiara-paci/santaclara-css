#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,time,datetime,sys

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from santaclara_css.models import CssColor,CssColorVariable

class Command(BaseCommand):
    args = '<name> <color>'
    help = 'Add color'

    def handle(self, *args, **options):
        color_name=args[0]
        color_desc=args[1]

        if color_desc[0]=="#":
            alpha=1.0
            color_obj,created=CssColor.objects.get_or_create(hexadecimal=color_desc[1:],
                                                             defaults={"name": color_desc})
            if created:
                print "Added color %s" % (unicode(color_obj))
        elif color_desc[:3]=="rgb":
            c=color_desc[3:-1]
            if c[0]=="a":
                c=c[2:]
                alpha=0
            else:
                c=c[1:]
                alpha=1
            t=c.split(",")
            r=int(t[0])
            g=int(t[1])
            b=int(t[2])
            if not alpha:
                alpha=float(t[3])
            color_obj,created=CssColor.objects.get_or_create(red=r,green=g,blue=b,
                                                            defaults={"name": color_desc})
            if created:
                print "Added color %s" % (unicode(obj))
        else:
            print "%s not valid" % color_desc
            return

        var_obj,created=CssColorVariable.objects.get_or_create(name=color_name,
                                                               defaults={"color":color_obj,"alpha":alpha})
        if created:
            print "Added %s=%s" % (var_obj.name,unicode(var_obj))

