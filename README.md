#Santa Clara Css

Santa Clara Css is a simple Django app to help managing css. 

##Quick start

1. Build package:
   ```
        $ cd santaclara-css/
        $ python setup.py sdist
   ```

2. Install package:
    ```
        $ cd santaclara-css/
        $ pip install --user dist/santaclara_css-<version>.tar.gz
    ```

3. Add "santaclara_css" to your INSTALLED_APPS setting like this:
    ```
        INSTALLED_APPS = (
            ...
            'santaclara_css',
            ...
        )
    ```

4. Add "template_vars_delegate" to TEMPLATE_CONTEXT_PROCESSORS setting like this:
    ```
	TEMPLATE_CONTEXT_PROCESSORS = (
            ...
	    "santaclara_css.template_vars_delegate.app_delegate",
            ...
        )
    ```	

5. Add DELEGATED_TEMPLATE_CONTEXT_PROCESSORS to settings.py:

    ```
        DELEGATED_TEMPLATE_CONTEXT_PROCESSORS = {
            'santaclara_css': (
                 'santaclara_css.context_processors.colors',
                 'santaclara_css.context_processors.shadows',
            )
        }
    ```

You can use DELEGATED_TEMPLATE_CONTEXT_PROCESSORS for your applications too.


##Documentation

- [Views](docs/views.md)
- [Template Tags](docs/css_tags.md)
- [Static files](docs/static.md)
- [Custom context processors](docs/context_processors.md)
- [Commands](docs/commands.md)
