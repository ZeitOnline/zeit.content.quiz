# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import copy

import zope.app.container.ordered
import zope.component
import zope.component.interfaces
import zope.interface

import zeit.cms.content.interfaces
import zeit.cms.content.xmlsupport
import zeit.connector.interfaces

import zeit.content.quiz.interfaces


class Container(zeit.cms.content.xmlsupport.XMLContentBase,
                zope.app.container.ordered.OrderedContainer):
    """Container that does not put its children in the repository.
    """

    zope.interface.implements(zeit.content.quiz.interfaces.IContainer)

    def __init__(self, xml_source=None):
        zeit.cms.content.xmlsupport.XMLContentBase.__init__(
            self, xml_source)
        zope.app.container.ordered.OrderedContainer.__init__(self)
        for xml_child in list(self._iter_xml_children()):
            try:
                child = zope.component.getAdapter(
                    fake_resource, zeit.cms.interfaces.ICMSContent,
                    name=xml_child.tag)
            except zope.component.interfaces.ComponentLookupError:
                continue
            child.xml = xml_child
            child.__name__ = xml_child.get('__name__')
            self[child.__name__] = child
            xml_child.getparent().remove(xml_child)

    def _iter_xml_children(self):
        return iter(self.xml['body'].getchildren())

    def copy_xml_tree(self):
        xml = copy.copy(self.xml)
        for child in self.values():
            if zeit.content.quiz.interfaces.IContainer.providedBy(child):
                xml_child = child.copy_xml_tree()
            else:
                xml_child = copy.copy(child.xml)
            xml_child.set('__name__', child.__name__)
            self._append_xml_child(xml, xml_child)
        return xml

    def _append_xml_child(self, xml, child):
        xml['body'].append(child)


class FakeResource(object):

    zope.interface.implements(zeit.connector.interfaces.IResource)

    data = None

fake_resource = FakeResource()


class FakeContent(object):

    zope.interface.implements(zeit.cms.content.interfaces.IXMLRepresentation)

    def __init__(self, xml):
        self.xml = xml


@zope.interface.implementer(zeit.cms.content.interfaces.IXMLSource)
@zope.component.adapter(Container)
def xml_source(context):
    xml = context.copy_xml_tree()
    return zeit.cms.content.interfaces.IXMLSource(FakeContent(xml))
