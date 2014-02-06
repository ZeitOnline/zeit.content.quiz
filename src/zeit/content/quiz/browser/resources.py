# Copyright (c) 2014 gocept gmbh & co. kg
# See also LICENSE.txt

from zeit.cms.browser.resources import Resource, Library
import zeit.cms.browser.resources


lib = Library('zeit.content.quiz', 'resources')
Resource('quiz.css')
Resource('quiz.js', depends=[
    zeit.cms.browser.resources.base, quiz_css])
