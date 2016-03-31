#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'prometheus-client>=0.0.13',
    'requests>=2.0',
    'xmltodict>=0.10.1',
    'click>=6.4',
]

test_requirements = [
    'pytest',
]

setup(
    name='kayako_exporter',
    version='0.1.0',
    description="Kayako metrics for Prometheus",
    long_description=readme + '\n\n' + history,
    author="MyBook",
    author_email='coagulant@mybook.ru',
    url='https://github.com/Eksmo/kayako-exporter',
    packages=['kayako_exporter',],
    package_dir={'kayako_exporter': 'kayako_exporter'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='kayako_exporter',
    entry_points="""
        [console_scripts]
        kayako_exporter=kayako_exporter:main
    """,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
