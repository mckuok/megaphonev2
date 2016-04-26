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