# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.viewlet.manager
import z3c.menu.ready2go
import z3c.menu.ready2go.manager

QuizAddMenu = zope.viewlet.manager.ViewletManager(
    'left', z3c.menu.ready2go.IAddMenu,
    bases=(z3c.menu.ready2go.manager.MenuManager,))
