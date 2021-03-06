#Custom context processors

You can define one or more function to populate the context. You nedd two steps.

1. Define one or more functions in your application (for example in
my_app/context_processors.py). The functions receive a request and return a
dictionary object (the keys become template variables):

```
def my_context_function_1(request=None):
    T={}
    ...
    return T

def my_context_function_2(request=None):
    T={}
    ...
    return T

...

```

2. Register your application and functions in DELEGATED_TEMPLATE_CONTEXT_PROCESSORS (settings.py):

```
DELEGATED_TEMPLATE_CONTEXT_PROCESSORS = { 
    ...
    'my_app': (
        'my_app.context_processors.my_context_function_1',
        'my_app.context_processors.my_context_function_2',
        ...
        )
    ...
    }
```
