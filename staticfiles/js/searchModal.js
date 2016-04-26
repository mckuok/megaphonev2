/**************************************
TODO
Check data exists before making another get request

************************************/

var subscribedDomainNames = [];
var subscribedPageNames = [];

function populateModal() {
    document.getElementById("subscribeDomain").disabled = true;
    document.getElementById("subscribePage").disabled = true;
    var domainList = [];
    var domainData = [];
    $.get("/get/domain", function(data) {
        domainData = JSON.parse(data);
        for (var i = 0; i < domainData.length; i ++) {
            domainList.push(domainData[i].fields.name);
        }
        console.log(domainList);
    }).then(function() {
        populateLikablePages(function(returnedValue) {
            subscribedDomainNames = returnedValue;
        });
        $('#search').modal('show');
        addAutoCompleteToSearchBox('#domainSearch', domainList, null, function(ui, sourceList, sourceData) {
            var button = document.getElementById("subscribeDomain");
            var selectedObj = ui.item;
            var domainName = document.getElementById("selectedDomainName");
            var domainDescription = document.getElementById("selectedDomainDescription");
            var memberNum = document.getElementById("selectedDomainMemberNumber");
            var selectedIndex = domainList.indexOf(selectedObj.value);
            domainName.innerHTML = selectedObj.value;
            domainDescription.innerHTML = domainData[selectedIndex].fields.description;
            memberNum.innerHTML = domainData[selectedIndex].fields.memberNum;
            console.log(subscribedDomainNames);
            if(subscribedDomainNames.indexOf(selectedObj.value) === -1) {
                button.innerHTML = "Subscribe";
                button.setAttribute("pk", domainData[selectedIndex].pk);
                button.disabled = false;
            } else {
                button.innerHTML = "Subscribed";
                button.disabled = true;
            }
        })
    });
}

function addAutoCompleteToSearchBox(inputID, sourceList, sourceData, selectFunction) {
    $( inputID ).autocomplete({
        source: sourceList,
        select: function( event, ui ) {
            selectFunction(ui, sourceList, sourceData);
        },
         minLength: 0,
         scroll: true
    }).focus(function() {
        $(this).autocomplete("search", "");
    });
}

function populateLikablePages(callback) {
    $.get("/get/pages", function(data) {
        subscribedPageNames = [];
        subscribedDomainNames = Object.keys(data);
        displayPageSearchBox(subscribedDomainNames);
        var subscribeDomainCount = subscribedDomainNames.length;
        for (var i = 0; i < subscribed_pages.length; i ++) {
            subscribedPageNames.push(subscribed_pages[i].fields.name);
        }
        for (var i = 0; i < subscribeDomainCount ; i ++) {
            var pageObject = JSON.parse(data[subscribedDomainNames[i]]);
            if (pageObject != null) {
                var pageList = [];
                var pageData = [];
                for (var j = 0; j < pageObject.length; j ++) {
                    pageData.push(pageObject[j]);
                    pageList.push(pageObject[j].fields.name);
                }
                addAutoCompleteToSearchBox("#page" + i, pageList, pageData, function(ui, sourceList, sourceData) {
                    for (var k = 0; k < subscribeDomainCount; k ++) {
                        $( "#page" + k).val('');
                    }
                    var button = document.getElementById("subscribePage");
                    var selectedObj = ui.item;
                    var pageName = document.getElementById("selectedPageName");
                    var pageDescription = document.getElementById("selectedPageDescription");
                    var memberNum = document.getElementById("selectedPageMemberNumber");
                    var selectedIndex = sourceList.indexOf(selectedObj.value);
                    pageName.innerHTML = selectedObj.value;
                    pageDescription.innerHTML = sourceData[selectedIndex].fields.description;
                    memberNum.innerHTML = sourceData[selectedIndex].fields.memberNum;
                    console.log(subscribedPageNames)
                    if(subscribedPageNames.indexOf(selectedObj.value) === -1) {
                        button.innerHTML = "Subscribe";
                        button.setAttribute("pk", sourceData[selectedIndex].pk);
                        button.disabled = false;
                    } else {
                        button.innerHTML = "Subscribed";
                        button.disabled = true;
                    }
                });
            }
        }
    }).then(function() {
         if(callback) {
            callback(subscribedDomainNames);
        }
    });
}

function displayPageSearchBox(domainNames) {
    var pageBlock = document.getElementById("likablePages");
    pageBlock.innerHTML = "";
    for(var i = 0; i < domainNames.length; i ++) {
        pageBlock.innerHTML = pageBlock.innerHTML.concat(
        '<div class="ui-widget"><label for="page' + i + '">' + domainNames[i] +
            ':&nbsp;</label><input type="text" id="page' + i + '" placeholder=" Select a page" /></div><br>');
    }
}

function subscribeDomainButton() {
    var button = document.getElementById("subscribeDomain");
    subscribeDomain(button.getAttribute("pk"), function() {
        populateLikablePages();
        button.innerHTML = "Subscribed";
        button.disabled = true;
    });

}

function subscribePageButton() {
    var button = document.getElementById("subscribePage");
    subscribePage(button.getAttribute("pk"), function() {
        // populateLikablePages();
        button.innerHTML = "Subscribed";
        button.disabled = true;
    });

}