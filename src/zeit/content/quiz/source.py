# -*- coding: utf-8 -*-
# Copyright (c) 2009 gocept gmbh & co. kg
# See also LICENSE.txt

import zeit.cms.content.contentsource
import zeit.content.quiz.interfaces


class QuizSource(zeit.cms.content.contentsource.CMSContentSource):
    """A source containing folders."""

    name = 'quiz'

    def verify_interface(self, value):
        return zeit.content.quiz.interfaces.IQuiz.providedBy(value)


quizSource = QuizSource()

