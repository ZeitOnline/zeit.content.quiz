# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import UserDict
import lxml.objectify
import zope.app.container.ordered
import zope.component
import zope.interface

import zeit.cms.content.interfaces
import zeit.cms.content.xmlsupport

import zeit.content.quiz.interfaces


class Container(UserDict.DictMixin):
    """Container that does not put its children in the repository.

    >>> import zope.interface.verify
    >>> zope.interface.verify.verifyClass(
    ...     zeit.content.quiz.interfaces.IContainer, Container)
    True

    """
    zope.interface.implements(zeit.content.quiz.interfaces.IContainer,
                              zeit.cms.content.interfaces.IXMLRepresentation)

    def __getitem__(self, name):
        for xml_child in self._iter_xml_children():
            if name == xml_child.get('__name__'):
                child = zope.component.getAdapter(
                    xml_child, zeit.cms.interfaces.ICMSContent,
                    name=xml_child.tag)
                zope.location.locate(child, self, name)
                return child
        else:
            raise KeyError(name)
    
    def __setitem__(self, name, obj):
        zope.location.locate(obj, self, name)
        obj.xml.set('__name__', name)
        self._append_xml_child(obj)

    def __delitem__(self, name):
        for xml_child in self._iter_xml_children():
            if name == xml_child.get('__name__'):
                xml_child.getparent().remove(xml_child)
                break
        else:
            raise KeyError(name)

    def keys(self):
        return [xml_child.get('__name__')
                for xml_child in self._iter_xml_children()]

    def _iter_xml_children(self):
        return iter(self.xml['body'].getchildren())

    def _append_xml_child(self, child):
        self.xml['body'].append(child.xml)


class Contained(zeit.cms.content.xmlsupport.XMLRepresentationBase,
                zope.app.container.contained.Contained):
    """Object in a container."""

    def __init__(self, xml_source=None, xml=None):
        super(Contained, self).__init__(xml_source=xml_source)
        if xml is not None:
            self.xml = xml
    

def xml_tree_content_adapter(factory):

    @zope.interface.implementer(zeit.cms.interfaces.ICMSContent)
    @zope.component.adapter(lxml.objectify.ObjectifiedElement)
    def adapter(context):
        return factory(xml=context)

    return adapter
