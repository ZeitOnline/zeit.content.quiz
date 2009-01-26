# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import copy
import inspect
import zc.form.field
import zeit.cms.content.field
import zeit.cms.content.interfaces
import zope.app.container.interfaces
import zope.interface
import zope.schema
from zeit.content.quiz.i18n import MessageFactory as _


class IReadContainer(zope.app.container.interfaces.IReadContainer,
                     zeit.cms.content.interfaces.IXMLRepresentation):
    """Read-only container that stores its children inside its own xml
    representation."""

    def content_modified():
        """Notify the container that content has changed."""


class IWriteContainer(zope.app.container.interfaces.IWriteContainer):
    """Writeable container that stores its children inside its own xml
    representation."""

    def updateOrder(order):
        """Revise the order of keys, replacing the current ordering.

        order is a list or a tuple containing the set of existing keys in
        the new order. `order` must contain ``len(keys())`` items and cannot
        contain duplicate keys.

        Raises ``TypeError`` if order is not a tuple or a list.

        Raises ``ValueError`` if order contains an invalid set of keys.

        Analogous to zope.app.container.interfaces.IOrderedContainer.
        """


class IReadQuiz(zeit.cms.content.interfaces.ICommonMetadata,
                zeit.cms.content.interfaces.IXMLContent,
                IReadContainer):
    """Read methods for quiz."""

    commentsAllowed = zope.schema.Bool(
        title=_("Comments allowed"),
        default=True)
    commentsAllowed.default = False


class IWriteQuiz(IWriteContainer):
    """Write methods for quiz."""


class IQuiz(IReadQuiz, IWriteQuiz):
    """Quiz content type."""


class IQuizContent(zope.interface.Interface):
    """Sub-objects of a quiz.
    """

    title = zope.schema.TextLine(
        title=_('Title'),
        description=_('quiz-content-title-description'),
        required=False)


class IReadQuestion(IQuizContent, IReadContainer):
    """Read methods for question."""

    question = zc.form.field.HTMLSnippet(
        title=_("Text"))


class IWriteQuestion(IWriteContainer):
    """Write methods for question."""


class IQuestion(IReadQuestion, IWriteQuestion):
    """Question content type."""


class OnlyOneMayBeCorrect(zope.schema.ValidationError):

    def doc(self):
        return _('Only one answer may be correct.')


def only_one_may_be_correct(value):
    if not value:
        # We're not correct, so that's good
        return True

    field = inspect.stack()[2][0].f_locals['self']
    answer = IAnswer(field.context, None)
    #if answer is None:
    question = IQuestion(field.context)

    for existing_answer in question.values():
        if existing_answer.correct and existing_answer != answer:
            raise OnlyOneMayBeCorrect()

    return True


class IAnswer(zeit.cms.content.interfaces.IXMLRepresentation, IQuizContent):
    """Answer content type."""

    correct = zope.schema.Bool(
        title=_('Correct?'),
        constraint=only_one_may_be_correct)

    answer = zc.form.field.HTMLSnippet(
        title=_("Text"))


class IQuizUpdater(zope.interface.Interface):
    """Update the quiz in the actual quiz system."""

    def update():
        """Update the quiz for preview.

        Note that update() will create a quiz instance in the remote system
        implicily if there is none.

        """
