var subscribed_domains;
var subscribed_pages;

function getSubscribedDomains(callback) {
    $.get("/subscribe/domain/", function(data) {
        subscribed_domains = JSON.parse(data);
    }).done(function() {
        if (callback) {
            callback();
        }
    })
}

function getSubscribedPages(callback) {
    $.get("/subscribe/page/", function(data) {
        subscribed_pages = JSON.parse(data);
    }).done(function() {
        if (callback) {
            callback();
        }
    })
}

function subscribeDomain(pk, callback) {
    var url = "/subscribe/domain/" + pk + "/";
    var newDomain;
    $.ajax({
        type: "POST",
        url: url,
        success : function(data) {
            newDomain = JSON.parse(data);
        },
        error : function(xhr,errmsg,err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    }).done(function() {
        subscribed_domains.push(newDomain[0]);
        if (callback) {
            callback();
        }
    });
}

function subscribePage(pk, callback) {
    var url = "/subscribe/page/" + pk + "/";
    var newPage;
    $.ajax({
        type: "POST",
        url: url,
        success : function(data) {
            newPage = JSON.parse(data);
        },
        error : function(xhr,errmsg,err) {
            alert(xhr.status + ": " + xhr.responseText);
        }
    }).done(function() {
        subscribed_pages.push(newPage[0]);
        subscribedPageNames.push(newPage[0].fields.pageName);
        if (callback) {
            callback();
        }
    });
}