# Copyright (c) 2009 gocept gmbh & co. kg
# See also LICENSE.txt

import zeit.cms.content.contentsource
import zeit.content.quiz.interfaces


class QuizSource(zeit.cms.content.contentsource.CMSContentSource):
    """A source containing folders."""

    name = 'quiz'
    check_interfaces = (zeit.content.quiz.interfaces.IQuiz,)


quizSource = QuizSource()
