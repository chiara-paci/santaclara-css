# Create your views here.

from django.views.generic import TemplateView

from django import http

class CssTemplateView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(CssTemplateView, self).render_to_response(context,content_type='text/css', **kwargs)

