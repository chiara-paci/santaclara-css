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

