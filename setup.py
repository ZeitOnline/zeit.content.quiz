# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages

setup(
    name='zeit.content.quiz',
    version='0.5.9.dev0',
    author='gocept',
    author_email='mail@gocept.com',
    url='https://svn.gocept.com/repos/gocept-int/zeit.cms/zeit.content.quiz',
    description="""\
""",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='gocept proprietary',
    namespace_packages=['zeit', 'zeit.content'],
    install_requires=[
        'gocept.form',
        'lxml',
        'rwproperty',
        'setuptools',
        'z3c.etestbrowser',
        'zc.form',
        'zeit.cms>=2.20.0.dev0',
        'zeit.content.quiz',
        'zeit.connector',
        'zeit.wysiwyg',
        'zope.annotation',
        'zope.app.container',
        'zope.app.pagetemplate',
        'zope.app.securitypolicy',
        'zope.app.zcmlfiles',
        'zope.cachedescriptors',
        'zope.component',
        'zope.event',
        'zope.formlib',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.location',
        'zope.publisher',
        'zope.schema',
        'zope.security',
        'zope.testing',
        'zope.traversing',
    ],
    entry_points={
        'fanstatic.libraries': [
            'zeit_content_quiz=zeit.content.quiz.browser.resources:lib',
        ],
    },
)
