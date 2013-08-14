"""
Flask-Gzip
------------

Compress responses in your Flask app with gzip..
"""

from setuptools import setup

setup(
    name='Flask-Gzip',
    version='0.9',
    url='https://github.com/wichitacode/flask-gzip',
    license='MIT',
    author='William Fagan',
    author_email='will@wichitacode.com',
    description='Compress responses in your Flask app with gzip.',
    long_description=__doc__,
    py_modules=['flask_gzip'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
