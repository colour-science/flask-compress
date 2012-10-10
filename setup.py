"""
Flask-gzip
------------

Flask extension to compress all of your application's responses using gzip.
"""

from setuptools import setup

setup(
    name='Flask-gzip',
    version='0.1',
    url='https://github.com/elasticsales/flask-gzip',
    license='BSD',
    author='Anthony Nemitz',
    author_email='anemitz@gmail.com',
    description='Compress responses in your Flask app with gzip.',
    long_description=__doc__,
    py_modules=['flask_gzip'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['Flask'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
