// Copyright (c) 2008-2009 gocept gmbh & co. kg
// See also LICENSE.txt

MochiKit.Signal.connect(window, 'onload', function() {
    var questions = getFirstElementByTagAndClassName('ol', 'questions');
    if (! questions) {
        return;
    }

    var class_names = ['answers', 'questions']; // order is important
    forEach(class_names, function(class_name) {
        forEach(getElementsByTagAndClassName('ol', class_name),
                function(list) {
            MochiKit.Sortable.Sortable.create(
                list.id, {
                only: ['question', 'answer']
            });
        });
    });

    MochiKit.Signal.connect(MochiKit.DragAndDrop.Draggables, 'end',
                            function (event) {
                                event.element.dragging = true;
                            });

    MochiKit.Signal.connect(questions, 'onclick', function(event) {
        var item = getFirstParentByTagAndClassName(event.target(), 'li');
        if (item.dragging) {
            event.stop();
            item.dragging = false;
        };
    });
});
