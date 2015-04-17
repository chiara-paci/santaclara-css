import os
from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='santaclara_css',
    version='0.7.1.1',
    packages=['santaclara_css'],
    package_data={'santaclara_css': [
            'static/santaclara_css/*.css',
            'templatetags/*',
            'templates/santaclara_css/*',
            'management/*.py',
            'management/commands/*',
            'fixtures/*'
            ]},
    include_package_data=True,
    license='GNU General Public License v3 or later (GPLv3+)',  # example license
    description='A simple Django app to write css',
    long_description=README,
    url='http://www.gianoziaorientale.org/software/',
    author='Gianozia Orientale',
    author_email='chiara@gianziaorientale.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
