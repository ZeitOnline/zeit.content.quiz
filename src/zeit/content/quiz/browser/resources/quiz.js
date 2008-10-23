// Copyright (c) 2008 gocept gmbh & co. kg
// See also LICENSE.txt

if (typeof(zeit.content) == 'undefined') {
    zeit.content = {};
}

if (typeof(zeit.content.quiz) == 'undefined') {
    zeit.content.quiz = {};
}


zeit.content.quiz.Sorter = Class.extend({
    // sort questions and answers

    construct: function(class_names) {
        var othis = this;
        othis.dragging = false;

        function handle(item) {
            new Draggable(item, {
                ghosting: true
            });

//                 // Disable click event while dragging.
//                 connect(item, 'onclick', function(event) {
//                         alert(event.target().nodeName);
//                     if ( othis.dragging == true) {
//                             event.stop();
//                         }
//                     });

            new Droppable(item, {
                ondrop: function (element) {
                    var parent = element.parentNode;
                    othis.dragging = true;
                    if (parent.nodeName != 'OL') {
                        // TODO: i18n
                        alert('The list can only be sorted. ' +
                              'Adding is not possible.')
                        return;
                    }
                    var anchor = item.nextSibling;
                    while (anchor && anchor.nodeName != 'LI')
                        anchor = anchor.nextSibling;
                    parent.insertBefore(element, anchor);
                    element.setAttribute('style', '');
                },
                hoverclass: 'questionsort-hover',
            });
        }

        forEach(class_names, function(class_name) {
            forEach(getElementsByTagAndClassName('ol', class_name),
                    function(list) {
                forEach(list.childNodes, function(node) {
                    if (node.nodeName == 'LI') {
                        handle(node);
                    };
                });
            });
        });
    },
});

connect(window, "onload", function() {
    new zeit.content.quiz.Sorter(['questions', 'answers']);
});
