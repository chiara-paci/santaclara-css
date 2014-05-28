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

##Documentation

- [Views](docs/views.txt)
- [Template Tags](docs/css_tags.txt)
- [Static files](docs/static.txt)
