#! /usr/bin/python
# -*- coding: utf-8 -*-

import re,time,datetime,sys

from django.core.management.base import BaseCommand

from santaclara_css.models import CssEquivalenceStanza

class Command(BaseCommand):
    help = 'Update css stanzas'

    def handle(self, *args, **options):
        for obj in CssEquivalenceStanza.objects.all():
            obj.save()
        
