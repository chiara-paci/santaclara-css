from django.conf.urls import patterns, include, url
from django.conf import settings
#from django.views.generic import simple

from santaclara_css.views import CssTemplateView,AllVarsView,CssEquivalenceStanzaView

urlpatterns =patterns('',
                      ( r'base.css$',        CssTemplateView.as_view(template_name='santaclara_css/base.css') ),
                      ( r'equivalence.css$', CssEquivalenceStanzaView.as_view() ),
                      ( r'allvars$',         AllVarsView.as_view() ),
                      )



