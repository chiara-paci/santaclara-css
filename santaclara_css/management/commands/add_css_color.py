#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,time,datetime,sys

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from santaclara_css.models import CssColor

class Command(BaseCommand):
    args = '<name> <color>'
    help = 'Add color'

    def handle(self, *args, **options):
        color_name=args[0]
        color_desc=args[1]

        if color_desc[0]=="#":
            obj,created=CssColor.objects.get_or_create(name=color_name,
                                                       defaults={"hexadecimal": color_desc[1:]})
            if created:
                print "Added color %s=%s" % (color_name,unicode(obj))
            else:
                print "Color %s already exists (%s)" % (color_name,unicode(obj))
            return

        if color_desc[:3]=="rgb":
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
            obj,created=CssColor.objects.get_or_create(name=color_name,
                                                       defaults={"red": r,"green":g,"blue":b,"alpha":alpha})
            if created:
                print "Added color %s=%s" % (color_name,unicode(obj))
            else:
                print "Color %s already exists (%s)" % (color_name,unicode(obj))



