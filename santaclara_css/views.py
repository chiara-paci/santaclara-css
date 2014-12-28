# Create your views here.

from django.views.generic import TemplateView

from django import http

import template_vars_delegate

class CssTemplateView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(CssTemplateView, self).render_to_response(context,content_type='text/css', **kwargs)

class AllVarsView(TemplateView): 
    template_name = "santaclara_css/variable_list.html"

    def get(self,request,*args,**kwargs):
        T=template_vars_delegate.app_delegate(request).items()
        T.sort()
        return render(request, self.template_name, {"variable_list":T})
        
    
