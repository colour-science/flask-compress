"""
Flask-Compress
------------

Compress responses in your Flask app with gzip..
"""

from setuptools import setup

setup(
    name='Flask-Compress',
    version='1.1.0',
    url='https://github.com/wichitacode/flask-compress',
    license='MIT',
    author='William Fagan',
    author_email='will@wichitacode.com',
    description='Compress responses in your Flask app with gzip.',
    long_description=__doc__,
    py_modules=['flask_compress'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    test_suite='tests',
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
