$(document).ready(function() {
    makeCalendar();
    $('#calendar-modal').on('shown.bs.modal', function () {
       $("#calendar").fullCalendar('render');
    });
});


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



function makeCalendar() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,basicWeek,basicDay'
        },
        defaultDate: moment().format('YYYY-MM-DD'),
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        aspectRatio: 2  ,
        events: globals.event_list,
        eventStartEditable: false,
        eventClick: function(calEvent, jsEvent, view) {

            var start = new Date(calEvent.start);
            var end = new Date(calEvent.end);
            var now = Date.now();
            var status = "";
            if (now > end) {
                status = "(Finished)";
            } else if (start < now && now < end){
                status = "(Ongoing)"
            }

            var level = capitalizeFirstLetter(calEvent.level) + " " + status;
            $('#event-name').text(calEvent.title);
            $('#event-host').text(calEvent.host);
            $('#event-type').text(calEvent.function);
            $('#event-location').text(calEvent.location);
            $('#event-start').text(formatDate(start));
            $('#event-end').text(formatDate(end));
            $('#event-description').text(calEvent.description);
            $('#event-watchers').text(calEvent.watchers);
            $('#event-goers').text(calEvent.goers);
            $('#event-level').text(level);
            document.getElementById("event-modal-header").style.backgroundColor = calEvent.color;
            $('#display-event').modal();
        }
    });
}


function capitalizeFirstLetter(word) {
    return word.charAt(0).toUpperCase() + word.substring(1)
}

