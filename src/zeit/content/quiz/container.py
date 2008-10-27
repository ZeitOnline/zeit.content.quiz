# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import UserDict
import lxml.objectify
import zope.app.container.interfaces
import zope.component
import zope.interface
import zope.lifecycleevent

import zeit.cms.content.xmlsupport

import zeit.content.quiz.interfaces


class Container(UserDict.DictMixin):
    """Container that does not put its children in the repository.

    >>> import zope.interface.verify
    >>> zope.interface.verify.verifyClass(
    ...     zeit.content.quiz.interfaces.IReadContainer, Container)
    True
    >>> zope.interface.verify.verifyClass(
    ...     zeit.content.quiz.interfaces.IWriteContainer, Container)
    True

    """
    zope.interface.implements(zeit.content.quiz.interfaces.IReadContainer,
                              zeit.content.quiz.interfaces.IWriteContainer)

    def __getitem__(self, name):
        for xml_child in self._iter_xml_children():
            if name == xml_child.get('name'):
                child = zope.component.getAdapter(
                    xml_child, zeit.cms.interfaces.ICMSContent,
                    name=xml_child.tag)
                zope.location.locate(child, self, name)
                return child
        else:
            raise KeyError(name)

    def __setitem__(self, name, obj):
        zope.location.locate(obj, self, name)
        obj.xml.set('name', name)
        self._append_xml_child(obj)
        self.content_modified()

    def __delitem__(self, name):
        for xml_child in self._iter_xml_children():
            if name == xml_child.get('name'):
                xml_child.getparent().remove(xml_child)
                break
        else:
            raise KeyError(name)
        self.content_modified()

    def keys(self):
        return [xml_child.get('name')
                for xml_child in self._iter_xml_children()]

    def _iter_xml_children(self):
        return iter(self.xml.getchildren())

    def _append_xml_child(self, child):
        self.xml.append(child.xml)

    def content_modified(self):
        self._get_persistent_container()._p_changed = True

    def _get_persistent_container(self):
        raise NotImplementedError

    def updateOrder(self, order):
        new_keys = set(order)
        if len(new_keys) != len(order):
            raise ValueError("Duplicate keys.")
        if new_keys != set(self.keys()):
            raise ValueError(
                "New order has different keys than are currently used.")
        children = dict(self.items())
        for key in order:
            # ElementTree does the Right Thing.
            self[key] = children[key]

    def __repr__(self):
        return object.__repr__(self)


class Contained(zeit.cms.content.xmlsupport.XMLRepresentationBase,
                zope.app.container.contained.Contained):
    """Object in a container."""

    def __init__(self, xml_source=None, xml=None):
        super(Contained, self).__init__(xml_source=xml_source)
        if xml is not None:
            self.xml = xml


@zope.component.adapter(Contained, zope.lifecycleevent.IObjectModifiedEvent)
def content_modified(context, event):
    context.__parent__.content_modified()


def xml_tree_content_adapter(factory):

    @zope.interface.implementer(zeit.cms.interfaces.ICMSContent)
    @zope.component.adapter(lxml.objectify.ObjectifiedElement)
    def adapter(context):
        return factory(xml=context)

    return adapter
