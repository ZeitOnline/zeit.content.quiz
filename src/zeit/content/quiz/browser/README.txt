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
>>> browser.getControl('Title').value = 'first question'
>>> browser.getControl('Question').value = '<a/>'
>>> browser.getControl('Add').click()

Adding a question redirects (for the moment) to the questions overview
where a link to the question is shown:

>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'
>>> browser.getLink('first question')
<Link text='first question' url='http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question'>




Checkin
=======

Check in the quiz:

>>> browser.getLink('Checkin').click()

We now have a view tab:

>>> browser.getLink('View metadata').click()
>>> print browser.contents
<?xml ...
<!DOCTYPE ...
<title> kochen – View quiz metadata </title>...
