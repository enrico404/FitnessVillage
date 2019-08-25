function courseClick(course){
    window.location.href = 'corso/'+course;
}

function getTime(){
    var today = new Date();
    var hour = today.getHours();
    var min = today.getMinutes();
    var sec = today.getSeconds();
    hour = this.formatTime(hour);
    min = this.formatTime(min);
    sec = this.formatTime(sec);
    document.getElementById('hours').innerText = hour;
    document.getElementById('min').innerText = min;
    document.getElementById('sec').innerText = sec;
    window.setTimeout("getTime()", 1000);

}

function formatTime(i){
    if(i < 10){
        i = "0"+i;

    }
    return i;
}
