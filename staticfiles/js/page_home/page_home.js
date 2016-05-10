$(document).ready(function() {
    globals.current_announcement = globals.current_announcement.replace(/&lt;br&gt;/g, "<br>");
    document.getElementById('current-announcement').innerHTML = globals.current_announcement;

    $('.announcement-content-text').each(function(i, obj) {
        var text = obj.innerHTML;
        text = text.replace(/&lt;br&gt;/g, "<br>");
        obj.innerHTML = text;
    });

    document.getElementById('new_announcement_button').disabled = true;
    minimizeText('minimizeCurrent', 400);
    $(document).on('mouseenter', '.current-announcement-board   ', function () {
                    $(this).find(":button").show();
                }).on('mouseleave', '.current-announcement-board', function () {
                    $(this).find(":button").hide();
                });
})

function postAnnouncementButton() {
    var button = document.getElementById('new_announcement_button');
    button.disabled = true;
    var text = document.getElementById('new_announcement');
    var input = text.value;
    input = input.replace(/\r?\n/g, '<br>');
    postAnnouncement('page', input, $('#new-announcement-title').val(), function() {
        getAnnouncements(1, 'page', 'self', function() {
            document.getElementById('current-announcement').innerHTML = announcements[0].fields.text;
            document.getElementById('current-announcement-title').innerHTML = announcements[0].fields.title;

            minimizeText('minimizeCurrent', 400);
            var date = new Date(announcements[0].fields.date_created);
            document.getElementById('current-announcement-date').innerHTML = formatDate(date);
            text.value = "";
            $('#new-announcement-title').val("")
            $('#new_announcement_input_panel').modal('hide');
    })});
}

function stoppedTyping(){
    var text = document.getElementById('new_announcement');
    if(text.value.length > 0) {
        document.getElementById('new_announcement_button').disabled = false;
    } else {
        document.getElementById('new_announcement_button').disabled = true;
    }
}

function announcementHistoryButton() {
    var button = document.getElementById('history_announcement_button');
    getAnnouncements(-1, 'page', 'self', function() {
        var board = document.getElementById('announcement-history-board');
        board.innerHTML = populateHistoryAnnouncementPage(0);
        minimizeText('minimizeHistory', 350);
        if (announcements.length > 5) {
            var pages = document.getElementById('historyPages');
            var totalAmount = Math.ceil(announcements.length / 5.0);
            text = '<ul class="pagination pagination-lg">';
            for (var i = 1; i <= totalAmount; i ++) {
                text = text.concat("<li><a id='historyPage", i , "' href='#'>", i, "</a></li>")
            }
            pages.innerHTML = text;

            for (var i = 1; i <= totalAmount; i ++) {
                $("#historyPage" + i).click(function() {
                    board.innerHTML = populateHistoryAnnouncementPage((parseInt(this.id.substring(11))-1)*5);
                    minimizeText('minimizeHistory', 350);
                });
            }
        }
        $('#history').modal('show');
        ;
    })
}

function formatDate(date) {
    var months = ['January', 'February' , 'March', 'April', 'May', 'June', 'July', 'August', 'September',
    'October', 'November', 'December'];
    var month = months[date.getMonth()];
    var hour = date.getHours();
    var stamp = 'a.m.';
    if(hour > 12) {
        hour = hour - 12;
        stamp = 'p.m.';
    }
    var minute =  date.getMinutes() < 10 ?  "0"  + date.getMinutes() :  date.getMinutes();
    return month + " " + date.getDate() + ", " +
                date.getFullYear() + ", " + hour + ":" +  minute + " " + stamp;
}

function populateHistoryAnnouncementPage(start) {
    var text = '<table class="table table-striped"><tbody>';
    var limit = start + 5 < announcements.length ? start + 5 : announcements.length ;

    for (var i = start; i < limit; i++) {
        text = text.concat("<tr><td><h3>", announcements[i].fields.title, "</h3>", "<p class='minimizeHistory'>",
        announcements[i].fields.text, "</p><p style='float:right;'>",
        formatDate(new Date(announcements[i].fields.date_created)),
            "</p></td></tr>");
    }
    text = text.concat('</tbody></table>');
    return text;
}