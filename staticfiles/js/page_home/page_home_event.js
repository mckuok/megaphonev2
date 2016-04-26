function createEventButton() {
    var dictionary = {
        role: 'page',
        name: $('#event-name').val(),
        date_event: new Date($('#event-start-date').val() + ' ' + $('#event-start-time').val()),
        date_end: new Date($('#event-end-date').val() + ' ' + $('#event-end-time').val()),
        location: $('#event-location').val(),
        func: $('#event-type').val(),
        description: $('#event-description').val()
    };

    postEvent(dictionary, function() {
         location.reload();
    });

}