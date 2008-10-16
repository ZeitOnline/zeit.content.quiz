# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import lxml.objectify

import zope.app.container.ordered
import zope.component
import zope.interface

import zeit.cms.content.interfaces
import zeit.cms.content.xmlsupport

import zeit.content.quiz.interfaces


class Container(zeit.cms.content.xmlsupport.XMLContentBase,
                zope.app.container.ordered.OrderedContainer):
    """Container that does not put its children in the repository.

    >>> import zope.interface.verify
    >>> zope.interface.verify.verifyClass(
    ...     zeit.content.quiz.interfaces.IContainer, Container)
    True

    """

    zope.interface.implements(zeit.content.quiz.interfaces.IContainer)

    def __init__(self, xml_source=None, xml=None):
        zeit.cms.content.xmlsupport.XMLContentBase.__init__(
            self, xml_source)
        zope.app.container.ordered.OrderedContainer.__init__(self)
        if xml is not None:
            self.xml = xml
        for xml_child in list(self._iter_xml_children()):
            child = zope.component.getAdapter(
                xml_child, zeit.cms.interfaces.ICMSContent,
                name=xml_child.tag)
            self[xml_child.get('__name__')] = child

    def _iter_xml_children(self):
        return iter(self.xml['body'].getchildren())

    def __setitem__(self, name, obj):
        super(Container, self).__setitem__(name, obj)
        obj.xml.set('__name__', name)
        self._append_xml_child(obj)

    def _append_xml_child(self, child):
        self.xml['body'].append(child.xml)

    def __delitem__(self, name):
        raise NotImplementedError


def xml_tree_content_adapter(factory):

    @zope.interface.implementer(zeit.cms.interfaces.ICMSContent)
    @zope.component.adapter(lxml.objectify.ObjectifiedElement)
    def adapter(context):
        return factory(xml=context)

    return adapter
