$(document).ready(function() {
    makeCalendar();
    $('#calendar-modal').on('shown.bs.modal', function () {
       $("#calendar").fullCalendar('render');
    });
});


function createEventButton() {

    var dictionary = {
        role: 'domain',
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

function allHistoryButton() {
    var board = document.getElementById('all-event-board')
    getEvents(-1, 'page', 'any', function(events) {
        for(var i = 0; i < events.length; i++) {
            var text = "";
            var name = events[i].fields.name;
            var location = events[i].fields.location;
            var type = events[i].fields.function;
            var start = formatDate(new Date(events[i].fields.date_event));
            var end = formatDate(new Date(events[i].fields.date_end));
            var description = events[i].fields.description;
            var watchers = events[i].fields.watchers;
            var goers = events[i].fields.goers;
            var pk = events[i].fields.object_id;
            var page;
            $.get("/get/pages/?pk=" + pk, function(data) {
                page = JSON.parse(data)[0];
                console.log(page)
            }).done(function() {
                text = text.concat(
                '<div class="single-event"><p class="event-header" type="button" data-toggle="collapse" data-target="#',
                    name, '_history"> ', name, '</p>',
                    '<div id="', name, '_history" class="single-event-content collapse">',
                    '<div class="row"><div class="col-sm-6">',
                    '<p><strong>Organizer:</strong> ', page.fields.name, '</p>',
                    '<p><strong>Type of Event:</strong> ', type, '</p>', '</div>',
                    '<div class="col-sm-6">', '<p><strong>Location:</strong> ', location, '</p>',
                    '<p><strong>Start:</strong> ', start, '</p>',
                    '<p><strong>End:</strong> ', end, '</p>', '</div>', '</div>',
                    '<p><strong>About:</strong> ', description, '</p>',
                    '<p class="event-counters"><strong>Watching:</strong> ', watchers,
                    ' <strong>Going:</strong>', goers, '</p></div></div>');
                board.innerHTML = board.innerHTML.concat(text);
            })
        }
        $('#eventHistory').modal('show');
    })

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





