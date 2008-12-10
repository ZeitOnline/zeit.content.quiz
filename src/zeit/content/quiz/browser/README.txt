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

After adding the quiz we're at its metadata view.

>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@edit.html'

The quiz has assets:

>>> browser.getLink('Edit assets')
<Link text='Edit assets' ...>


Add a question
--------------

We go to the questions overview of the quiz and add a question:

>>> browser.getLink('Questions').click()
>>> browser.getLink('Add question').click()

Suppose we did so by mistake; after we cancel adding the question, we are
taken back to the questions overview:

>>> browser.getControl('Cancel').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'

Let's now add a question. After that, we get redirected to the question's add
form for an answer:

>>> browser.getLink('Add question').click()
>>> browser.getControl('Title').value = 'first question'
>>> browser.getControl('Text').value = '<p>test</p>er'
>>> browser.getControl('Apply and add answer').click()
>>> print browser.contents
<?xml ...
 <title> first question – Add answer </title>
 ...
        <li class="message">Added question.</li>
        ...


Add an answer
-------------

Again, the user can decide to abort adding a answer, then he is sent back to
the answers view of the question:

>>> browser.getControl('Cancel').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'

Adding an answer redirects to the add form for the next answer:

>>> browser.getLink('Add answer').click()
>>> browser.getControl('Title').value = 'first answer'
>>> browser.getControl('Correct?').click()
>>> browser.getControl('Text').value = '<p>test</p>er'
>>> browser.getControl('Explanation').value = '<p>This is right.</p>'
>>> browser.getControl('Apply and add').click()
>>> print browser.contents
<?xml ...
 <title> first question – Add answer </title>
 ...
        <li class="message">Added answer.</li>
        ...
 


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
>>> print browser.title.strip()
kochen – Edit quiz

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

>>> browser.getControl('Title').value = '1st question & ans'
>>> browser.getControl('Text').value = '<p><em>foo</em> bar</p>'

We note that this question view does not have a check-in link:

>>> browser.getLink('Checkin')
Traceback (most recent call last):
LinkNotFoundError

After editing the question, we're on the questions overview tab of the quiz:

>>> browser.getControl('Apply').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'

Editing an answer
-----------------

Clicking on the links opens an edit form which contains the previously
entered values:

>>> browser.getLink('first answer').click()
>>> browser.getControl('Title').value
'first answer'
>>> browser.getControl('Correct?').selected
True
>>> browser.getControl('Text').value
'<p>test</p>er\r\n'
>>> browser.getControl('Explanation').value
'<p>This is right.</p>\r\n'

We note that the answer view does not have a check-in link either:

>>> browser.getLink('Checkin')
Traceback (most recent call last):
LinkNotFoundError

The question gets displayed:

>>> print browser.contents
<?xml version="1.0"?>
<!DOCTYPE ...
<fieldset...
  <legend>Question</legend>...
  <span>Title</span>...
  <div class="widget">1st question &amp; ans</div>...
  <span>Text</span>...
  <div class="widget">&lt;p&gt;&lt;em&gt;foo&lt;/em&gt; bar&lt;/p&gt; </div>...
</fieldset>...

These displayed values of the answer can be changed:

>>> browser.getControl('Title').value = '1st answer'
>>> browser.getControl('Correct?').click()
>>> browser.getControl('Correct?').selected
False
>>> browser.getControl('Text').value = ''
>>> browser.getControl('Explanation').value = '<p><em>This is really right.</em></p>'

As the text field is required we get an error message when we click on
apply:

>>> browser.getControl('Apply').click()
>>> print browser.contents
<?xml version="1.0"?>
<!DOCTYPE...
<li class="error">Text: Required input is missing.</li>...

After editing the answer, we're on the questions overview tab as well:

>>> browser.getControl('Text').value = '<p><em>foh</em> bah</p>'
>>> browser.getControl('Apply').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'

Questions and answers without a title
-------------------------------------

Questions and answers do not have to have a title. We can add both without
filling in the title field:

>>> browser.getLink('Add question').click()
>>> browser.getControl('Text').value = '<p>zweiter Test</p>er'
>>> browser.getControl('Apply and add').click()

>>> browser.getControl('Text').value = '<p>zweiter Test - Antwort</p>er'
>>> browser.getControl(name='form.actions.apply').click()
>>> print browser.title.strip()
kochen – Quiz overview

Later, we can also edit both without filling in the title:

>>> browser.getLink('zweiter Test').click()
>>> browser.getControl('Text').value = '<p><em>foo</em> bar</p>'
>>> browser.getControl('Apply').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'

>>> browser.getLink('zweiter Test - Antwort').click()
>>> browser.getControl('Text').value = '<p><em>ant</em> wort</p>'
>>> browser.getControl('Correct?').click()
>>> browser.getControl('Apply').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'


Re-ordering questions and answers
=================================

We can re-order questions and answers by using Drag-and-drop and then
submitting the form contained in the questions overview. In order to see the
effect on answers, we have to create another one:

>>> browser.getLink('Add answer', index=0).click()
>>> browser.getControl('Title').value = '2nd <answer>'
>>> browser.getControl('Text').value = '<p>foobar</p>'
>>> browser.getControl('Correct?').click()
>>> browser.getControl('Correct?').selected
True
>>> browser.getControl(name='form.actions.apply').click()

Before any re-ordering, questions and answers are listed in the questions
overview in the same order they were created:

>>> print browser.contents
<?xml version="1.0"?>
    ...
    <ol class="questions" id="sortable-questions">
      <li class="question">
        <a href="...">1st question &amp; ans</a>
        <input type="hidden" name="__quiz__:list"
               value="first question" />
        <ol class="answers" id="sortable-answers-0">
          <li class="answer">
            <span class="not-correct">
              (not correct)
            </span>
            <a href="...">1st answer</a>
            <input type="hidden" name="first question:list"
                   value="first answer" />
          </li>
          <li class="answer">
            <span class="correct">
              (correct)
            </span>
            <a href="...">2nd &lt;answer&gt;</a>
            <input type="hidden" name="first question:list"
                   value="2nd &lt;answer&gt;" />
          </li>
          <li class="add">
            <a href="...">
              Add answer
            </a>
          </li>
        </ol>
      </li>
      <li class="question">
        <a href="..."><p><em>foo</em> bar</p> </a>
        <input type="hidden" name="__quiz__:list"
               value="Question" />
        <ol class="answers" id="sortable-answers-1">
          <li class="answer">
            <span class="correct">
              (correct)
            </span>
            <a href="..."><p><em>ant</em> wort</p>
</a>
            <input type="hidden" name="Question:list"
                   value="Answer" />
          </li>
          <li class="add">
            <a href="...">
              Add answer
            </a>
          </li>
        </ol>
      </li>
      <li class="add">
        <a href="...">
          Add question
        </a>
      </li>
    </ol>
    ...

As re-ordering is done via drag'n'drop we submit only the result here:

>>> browser.open(
...     'http://localhost/++skin++cms/workingcopy/zope.user/kochen/'
...     '@@questions.html?apply=1&'
...     '__quiz__:list=Question&'
...     '__quiz__:list=first%20question&'
...     'first%20question:list=2nd%20<answer>&'
...     'first%20question:list=first%20answer&'
...     'Question:list=Answer')
>>> print browser.contents
<?xml version="1.0"?>
<!DOCTYPE...
<ol class="questions" id="sortable-questions">
 ...Question...
   ...Answer...
 ...1st question...
   ...2nd &lt;answer&gt;...
   ...1st answer...


Deleting questions and answers
==============================

Deleting a question or answer is done using a button on the item's edit form.

Deleting answers
----------------

Let's delete the untitled answer we just added:

>>> browser.open(
...     'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html')
>>> browser.getLink('ant wort').click()
>>> browser.getControl('Delete').click()
>>> print browser.contents
<?xml ...
 <title> kochen – Quiz overview </title>
    ...
    <li class="message">Item was deleted.</li>
    ...

>>> browser.getLink('ant wort')
Traceback (most recent call last):
LinkNotFoundError

Deleting questions
------------------

Let's delete the untitled question we just added:

>>> browser.open(
...     'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html')
>>> browser.getLink('foo bar').click()
>>> browser.getControl('Delete').click()
>>> browser.url
'http://localhost/++skin++cms/workingcopy/zope.user/kochen/@@questions.html'
>>> browser.getLink('foo bar', index=1)
Traceback (most recent call last):
LinkNotFoundError


Check-in
========

To check-in the quiz we have to go back to the quiz:

>>> browser.getLink('kochen').click()
>>> browser.getLink('Checkin').click()

We now have a view tab:

>>> browser.getLink('View metadata').click()
>>> print browser.title.strip()
kochen – View quiz


Checkout
========

Check out the quiz again:

>>> browser.getLink('Checkout').click()

The question we created before checking in the quiz is still there and
still has the same values:

>>> browser.getLink('Questions').click()
>>> browser.getLink('1st question')
<Link text='1st question & ans' url='http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/@@edit.html'>
>>> browser.getLink('1st question').click()
>>> browser.getControl('Title').value
'1st question & ans'
>>> browser.getControl('Text').value
'<p><em>foo</em> bar</p>\r\n'

The answer is still there and has the same values:

>>> browser.getLink('kochen').click()
>>> browser.getLink('Questions').click()
>>> browser.getLink('1st answer')
<Link text='1st answer' url='http://localhost/++skin++cms/workingcopy/zope.user/kochen/first%20question/first%20answer/@@edit.html'>
>>> browser.getLink('1st answer').click()
>>> browser.getControl('Title').value
'1st answer'
>>> browser.getControl('Text').value
'<p><em>foh</em> bah</p>\r\n'
>>> browser.getControl('Explanation').value
'<p>\r\n  <em>This is really right.</em>\r\n</p>\r\n'
