# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
"""Connection to the actual quiz system."""

import urllib
import urllib2
import zope.app.appsetup.product
import zope.interface
import zope.component
import zeit.content.quiz.interfaces


class Updater(object):

    zope.component.adapts(zeit.content.quiz.interfaces.IQuiz)
    zope.interface.implements(zeit.content.quiz.interfaces.IQuizUpdater)

    def __init__(self, context):
       self.context = context

    def update(self):
        url = self.get_url()
        if url:
            urllib2.urlopen(url, self.get_data())

    def get_url(self):
        config = zope.app.appsetup.product.getProductConfiguration(
            'zeit.content.quiz')
        if config:
            return config.get('url')

    def get_data(self):
        data = dict(
            quiz_id=self.context.uniqueId.replace('http://xml.zeit.de', '', 1),
            action='preview',
            xml=zeit.cms.content.interfaces.IXMLSource(self.context))
        return urllib.urlencode(sorted(data.items()))


@zope.component.adapter(
    zeit.content.quiz.interfaces.IQuiz,
    zeit.cms.checkout.interfaces.IAfterCheckinEvent)
def update_after_checkin(context, event):
    updater = zeit.content.quiz.interfaces.IQuizUpdater(context)
    updater.update()
