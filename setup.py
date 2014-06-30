import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_hautomation_suite',
    version='0.6',
    packages=['django_hautomation_suite', 'django_hautomation_suite.ha_cfg', ],
    include_package_data=True,
    license='BSD License',
    description='Django project to help deploy the Home Automation Python Project',
    long_description=README,
    url='http://blog.digitalhigh.es',
    author='Javier Pardo Blasco(jpardobl)',
    author_email='jpardo@digitalhigh.es',
    install_requires = (
      "Django==1.5",
      "django_hautomation",
      "hautomation_x10",
      "django_haweb",
      "django_thermostat",
      "simplejson==2.6.2",
      "requests==1.2.0",
      "pytz",
      "gunicorn",      
    ),
    #test_suite='hautomation_x10.tests.main',
    #tests_require=("selenium", "requests"),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Home Automation',
    ],
)
