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

        print color_name,color_desc
