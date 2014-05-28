#Views

##CssTemplateView

It's just a TemplateView with content_type='text/css'.

In any urls.py file, for example:
```
    urlpatterns =patterns('',
                          ...
                          ( r'base.css$', CssTemplateView.as_view(template_name='css/base.css') ),
	          	  ...
                          ) 
```
