#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,time,datetime,sys

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from santaclara_css.models import CssEquivalence,CssEquivalenceColorVariable

class Command(BaseCommand):
    args = '<name> <equivalence> <alpha>'
    help = 'Add equivalence'

    def handle(self, *args, **options):
        color_name=args[0]
        color_eq=args[1]
        color_alpha=float(args[2])

        equivalence=CssEquivalence.objects.get(name=color_eq)

        var,created=CssEquivalenceColorVariable.objects.get_or_create(name=color_name,
                                                                      defaults={ "equivalence": equivalence, "alpha": color_alpha })

        if created:
            print "Added %s=%s alpha=%2.2f" % (var.name,unicode(equivalence),alpha)

