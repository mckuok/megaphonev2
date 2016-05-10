
function getEvents(count, range, target, callback) {
    var events;
    var url = "/get/event/?count=" + count + "&range=" + range + "&target="+target;
     $.get(url, function(data) {
        events = JSON.parse(data);
    }).done(function() {
        if (callback) {
            callback(events);
        }
    });
}


function postEvent(dictionary, callback) {
    var url = "/create/event/";
    var arr = {
        role: dictionary.role,
        name: dictionary.name,
        date_event: dictionary.date_event,
        date_end: dictionary.date_end,
        location: dictionary.location,
        func: dictionary.func,
        description: dictionary.description
    };


    $.ajax({
        type: "POST",
        url: url,
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(arr),
        error : function(xhr,errmsg,err) {
            console.log(errmsg);
            alert(xhr.status + ": " + xhr.responseText);
        }
    }).done(function() {
        if (callback) {
            callback();
        }
    });
}

function joinEvent(pk, callback) {
    var url = "/attend/event/" + pk + '/';

    $.ajax({
        type: "POST",
        url: url,
        error : function(xhr,errmsg,err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    }).done(function() {
        if (callback) {
            callback();
        }
    });
}
