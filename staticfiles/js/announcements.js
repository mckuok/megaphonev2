var announcements;

function getAnnouncements(count, range, target, callback) {
    var url = "/get/announcement/?count=" + count + "&range=" + range + "&target="+target;
     $.get(url, function(data) {
        announcements = JSON.parse(data);
    }).done(function() {
        if (callback) {
            callback();
        }
    });
}

function postAnnouncement(role, text, title, callback) {
    var url = "/create/announcement/";
    var arr = {
        role: role,
        text: text,
        level: role,
        title: title
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