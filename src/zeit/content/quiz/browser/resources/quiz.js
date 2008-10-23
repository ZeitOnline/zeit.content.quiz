// Copyright (c) 2008 gocept gmbh & co. kg
// See also LICENSE.txt

MochiKit.Signal.connect(window, 'onload', function() {
    var class_names = ['answers', 'questions']; // order is important
    forEach(class_names, function(class_name) {
        forEach(getElementsByTagAndClassName('ol', class_name),
                function(list) {
            MochiKit.Sortable.Sortable.create(
                list.id, {hoverclass: 'questionsort-hover',
            });
        });
    });

    MochiKit.Signal.connect(MochiKit.DragAndDrop.Draggables, 'end',
                            function (event) {
                                event.element.dragging = true;
                            });

    var questions = getFirstElementByTagAndClassName('ol', 'questions');
    MochiKit.Signal.connect(questions, 'onclick', function(event) {
        var item = event._event.target.parentNode
        if (item.dragging) {
            event.stop();
            item.dragging = false;
        };
    });
});
