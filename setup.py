from setuptools import setup, find_packages

with open('README.md') as fl:
    LONG_DESCRIPTION = fl.read()

setup(
    name='Flask-Compress',
    use_scm_version=True,
    url='https://github.com/colour-science/flask-compress',
    license='MIT',
    author='Thomas Mansencal',
    author_email='thomas.mansencal@gmail.com',
    description='Compress responses in your Flask app with gzip, deflate or brotli.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'flask',
        'brotli'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
