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

After adding the quiz we're at the questions page where we can add
questions later on, for now the page is empty:

>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'

We can edit the metadata of the quiz on the edit tab:

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

Add a question
--------------

A question can be added using the questions view:

>>> browser.getLink('Questions').click()
>>> browser.getLink('Add question').click()

The user can decide to abort adding a question, then he is sent back
to the questions view:

>>> browser.getControl('Cancel').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'

Adding a question redirects (for the moment) to the questions overview
where a link to the question is shown:

>>> browser.getLink('Add question').click()
>>> browser.getControl('Title').value = 'first question'
>>> browser.getControl('Text').value = '<p>test</p>er'
>>> browser.getControl('Add').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'
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

Add an answer
-------------

An answer can be added in the edit view of a question:

>>> browser.getLink('first question').click()
>>> browser.getLink('Add answer').click()

The user can decide to abort adding a answer, then he is sent back
to the answers view:

>>> browser.getControl('Cancel').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/@@answers.html'

Adding an answer redirects (for the moment) to the answers overview
where a link to the answer is shown:

>>> browser.getLink('Add answer').click()
>>> browser.getControl('Title').value = 'first answer'
>>> browser.getControl('Text').value = '<p>test</p>er'
>>> browser.getControl('Add').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/@@answers.html'
>>> browser.getLink('first answer')
<Link text='first answer' url='http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/first%20answer/@@edit.html'>

Clicking on the links opens an edit form which contains the previously
entered values:

>>> browser.getLink('first answer').click()
>>> browser.getControl('Title').value
'first answer'
>>> browser.getControl('Text').value
'<p>test</p>er\r\n'

These values can be changed:

>>> browser.getControl('Title').value = '1st answer'
>>> browser.getControl('Text').value = '<p><em>foh</em> bah</p>'
>>> browser.getControl('Apply').click()


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
