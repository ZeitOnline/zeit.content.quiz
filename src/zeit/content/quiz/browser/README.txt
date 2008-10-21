=========
Quiz tool
=========

Quizes are basically a document which contains questions which again
contain answers.  Let's Create a browser first:

>>> from zope.testbrowser.testing import Browser
>>> browser = Browser()
>>> browser.addHeader('Authorization', 'Basic user:userpw')


Add a quiz
==========

To add a quiz we go to a folder:

>>> browser.open('http://localhost/++skin++cms/repository/online/2007/01')
>>> menu = browser.getControl(name='add_menu')
>>> menu.displayValue = ['Quiz']
>>> browser.open(menu.value[0])

We set the most important values:

>>> browser.getControl('File name').value = 'kochen'
>>> browser.getControl('Title').value = 'Koch-Quiz'
>>> browser.getControl('Ressort').displayValue = ['Gesundheit']
>>> browser.getControl('Daily newsletter').selected = True
>>> browser.getControl(name='form.authors.0.').value = 'Hans Sachs'
>>> browser.getControl(name="form.actions.add").click()

After adding the quiz we're at the add page for questions:

>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@addQuestion.html'

Add a question
--------------

First of all, the user can decide to abort adding a question and go back to
the questions overview of the quiz:

>>> browser.getControl('Cancel').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'

Let's now add a question. After that, we get redirected to the question's add
form for an answer:

>>> browser.getLink('Add question').click()
>>> browser.getControl('Title').value = 'first question'
>>> browser.getControl('Text').value = '<p>test</p>er'
>>> browser.getControl('Add').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/@@addAnswer.html'

Add an answer
-------------

Again, the user can decide to abort adding a answer, then he is sent back to
the answers view of the question:

>>> browser.getControl('Cancel').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/@@answers.html'

Adding an answer redirects to the add form for the next answer:

>>> browser.getLink('Add answer').click()
>>> browser.getControl('Title').value = 'first answer'
>>> browser.getControl('Correct?').click()
>>> browser.getControl('Text').value = '<p>test</p>er'
>>> browser.getControl('Add').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/@@addAnswer.html'


Editing a quiz
==============

Editing quiz metadata
---------------------

We can edit the metadata of the quiz on its edit tab. We have to move to the
quiz first; let's do so by using the breadcrumb menu:

>>> browser.getLink('kochen').click()
>>> browser.getLink('Edit metadata').click()
>>> browser.getControl('Title').value
'Koch-Quiz'
>>> print browser.contents
<?xml ...
<!DOCTYPE ...
<title> kochen – Edit quiz </title>...

There is no read only view of the metadata:

>>> browser.getLink('View metadata')
Traceback (most recent call last):
LinkNotFoundError

Editing a question
------------------

Exisiting questions can be reached from the Questions tab:

>>> browser.getLink('Questions').click()
>>> browser.getLink('first question')
<Link text='first question' url='http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/@@edit.html'>

Clicking on the links opens an edit form which contains the previously
entered values:

>>> browser.getLink('first question').click()
>>> browser.getControl('Title').value
'first question'
>>> browser.getControl('Text').value
'<p>test</p>er\r\n'

These values can be changed:

>>> browser.getControl('Title').value = '1st question'
>>> browser.getControl('Text').value = '<p><em>foo</em> bar</p>'
>>> browser.getControl('Apply').click()

Editing an answer
-----------------

After editing the question, we're on its answers overview tab:

>>> browser.getLink('first answer')
<Link text='first answer' url='http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/first%20answer/@@edit.html'>

Clicking on the links opens an edit form which contains the previously
entered values:

>>> browser.getLink('first answer').click()
>>> browser.getControl('Title').value
'first answer'
>>> browser.getControl('Correct?').selected
True
>>> browser.getControl('Text').value
'<p>test</p>er\r\n'

These values can be changed:

>>> browser.getControl('Title').value = '1st answer'
>>> browser.getControl('Correct?').click()
>>> browser.getControl('Correct?').selected
False
>>> browser.getControl('Text').value = '<p><em>foh</em> bah</p>'
>>> browser.getControl('Apply').click()


Questions and answers without a title
-------------------------------------

Questions and answers do not have to have a title. We can add both without
filling in the title field:

>>> browser.handleErrors = False

>>> browser.getLink('kochen').click()
>>> browser.getLink('Questions').click()
>>> browser.getLink('Add question').click()
>>> browser.getControl('Text').value = '<p>zweiter Test</p>er'
>>> browser.getControl('Add').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/Question/@@addAnswer.html'

>>> browser.getControl('Text').value = '<p>zweiter Test</p>er'
>>> browser.getControl('Add').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/Question/@@addAnswer.html'

Later, we can also edit both without filling in the title:

>>> browser.getLink('kochen').click()
>>> browser.getLink('Questions').click()
>>> browser.getLink('Question', index=1).click()
>>> browser.getControl('Text').value = '<p><em>foo</em> bar</p>'
>>> browser.getControl('Apply').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/Question/@@answers.html'

>>> browser.getLink('Answers').click()
>>> browser.getLink('Answer', index=1).click()
>>> browser.getControl('Text').value = '<p><em>foo</em> bar</p>'
>>> browser.getControl('Apply').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/Question/@@answers.html'


Deleting questions and answers
==============================

Deleting a question or answer is done using a button on the item's edit form.

Deleting questions
------------------

Let's delete the untitled question we just added:

>>> browser.open(
...     'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html')
>>> browser.getLink('Question', index=1).click()
>>> browser.getControl('Delete').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'
>>> browser.getLink('Question', index=1)
Traceback (most recent call last):
LinkNotFoundError


Check-in
========

To check-in the quiz we have to go back to the quiz:

>>> browser.getLink('kochen').click()
>>> browser.getLink('Checkin').click()

We now have a view tab:

>>> browser.getLink('View metadata').click()
>>> print browser.contents
<?xml ...
<!DOCTYPE ...
<title> kochen – View quiz metadata </title>...


Checkout
========

Check out the quiz again:

>>> browser.getLink('Checkout').click()

The question we created before checking in the quiz is still there and
still has the same values:

>>> browser.getLink('Questions').click()
>>> browser.getLink('first question')
<Link text='first question' url='http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/@@edit.html'>
>>> browser.getLink('first question').click()
>>> browser.getControl('Title').value
'1st question'
>>> browser.getControl('Text').value
'<p><em>foo</em> bar</p>\r\n'

The answer is still there and has the same values:

>>> browser.getLink('Answers').click()
>>> browser.getLink('first answer')
<Link text='first answer' url='http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/first%20answer/@@edit.html'>
>>> browser.getLink('first answer').click()
>>> browser.getControl('Title').value
'1st answer'
>>> browser.getControl('Text').value
'<p><em>foh</em> bah</p>\r\n'
