function minimizeText(name, limit) {
    var minimized_elements = $('p.' + name);
    minimized_elements.each(function(){
        var orgtext = "";
        var t = $(this).html();
        orgtext =  $(this).html();
        if(t.length >= limit) {
            $(this).html(
                t.slice(0,limit)+'<span>... </span><a href="#" class="more">More</a>'+
                '<span style="display:none;">'+ t.slice(limit,t.length)+'</span>'
            );
        } else if (occurrences($(this).html(), "<br>") >= 5) {
            var occurrence = nth_occurrence(t, "<br>", 5);
            $(this).html(
                t.slice(0, occurrence)+'<span> ... </span><a href="#" class="more">More</a>'+
                '<span style="display:none;">'+ t.slice(occurrence, t.length)+'</span>'
            );
        } else {
            return;
        }

        expandLongText(orgtext, this);
    });
}

function expandLongText(text, elements) {
    $('a.more', elements).click(function(event){
        event.preventDefault();
        var line = $(this).parent();
        document.getElementById('longText-modal-header').innerHTML = line.prev().html();
        text = text.replace("... More", "");
        document.getElementById('longtext-holder').innerHTML = text + "<br><p style='float: right'>" +
            line.next().html() + '</p><br>';
        $('#longtext').modal('show');
    })
}

function occurrences(string, subString, allowOverlapping) {

    string += "";
    subString += "";
    if (subString.length <= 0) return (string.length + 1);

    var n = 0,
        pos = 0,
        step = allowOverlapping ? 1 : subString.length;

    while (true) {
        pos = string.indexOf(subString, pos);
        if (pos >= 0) {
            ++n;
            pos += step;
        } else break;
    }
    return n;
}


function nth_occurrence (string, char, nth) {
    var first_index = string.indexOf(char);
    var length_up_to_first_index = first_index + 1;

    if (nth == 1) {
        return first_index;
    } else {
        var string_after_first_occurrence = string.slice(length_up_to_first_index);
        var next_occurrence = nth_occurrence(string_after_first_occurrence, char, nth - 1);

        if (next_occurrence === -1) {
            return -1;
        } else {
            return length_up_to_first_index + next_occurrence;
        }
    }
}