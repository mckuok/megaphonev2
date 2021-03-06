$(document).ready(function() {
    $('.content-text').each(function(i, obj) {
        var text = obj.innerHTML;
        text = text.replace(/&lt;br&gt;/g, "<br>");
        obj.innerHTML = text;
    });


    getSubscribedDomains(function() {
        getSubscribedPages(function() {
            logic();
        })
    })
});

function logic() {
    if (globals.noSubscription) {
        populateModal();
    }
    makeCalendar();

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
            var joinButton = document.getElementById('join-event-button')
            joinButton.setAttribute("pk", calEvent.pk);
            joinButton.disabled = calEvent.disable;
            document.getElementById("event-modal-header").style.backgroundColor = calEvent.color;
            $('#display-event').modal();
        }
    });
}

function capitalizeFirstLetter(word) {
    return word.charAt(0).toUpperCase() + word.substring(1)
}

function joinEventButton() {
    var button = document.getElementById('join-event-button')
    joinEvent(button.getAttribute("pk"), function() {
        $('#event-goers').text(parseInt($('#event-goers').text()) + 1);
    });
    button.disabled = true;
}
