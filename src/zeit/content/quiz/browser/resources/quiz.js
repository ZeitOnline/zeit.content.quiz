// Copyright (c) 2008 gocept gmbh & co. kg
// See also LICENSE.txt

connect(window, 'onload', function() {
    class_names = ['answers', 'questions']; // order is important
    forEach(class_names, function(class_name) {
        forEach(getElementsByTagAndClassName('ol', class_name),
                function(list) {
            MochiKit.Sortable.Sortable.create(
                list.id, {hoverclass: 'questionsort-hover',
            });
        });
    });
});
