# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

from setuptools import setup, find_packages

setup(
    name='zeit.content.quiz',
    version='0.1.0dev',
    author='gocept',
    author_email='mail@gocept.com',
    url='https://svn.gocept.com/repos/gocept-int/zeit.cms/zeit.content.quiz',
    description="""\
""",
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    license='gocept proprietary',
    namespace_packages = ['zeit', 'zeit.content'],
    install_requires=[
        'lxml',
        'setuptools',
        'z3c.menu.ready2go',
        'zeit.cms',
        'zeit.connector',
        'zope.annotation',
        'zope.app.container',
        'zope.app.pagetemplate',
        'zope.cachedescriptors',
        'zope.component',
        'zope.event',
        'zope.formlib',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.location',
        'zope.schema',
        'zope.traversing',
        ],
    extras_require={
        'test': [
            'z3c.etestbrowser',
            'zope.testing',
            'zope.app.zcmlfiles',
            'zope.app.securitypolicy',
            'zeit.connector',
            ],
        },
    )
