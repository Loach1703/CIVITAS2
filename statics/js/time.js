var date = new Date();
var hour = date.getHours();
var minute = date.getMinutes();
var day = date.getDate();
var year = date.getFullYear();
var month = date.getMonth();
var d0 = new Date();
d0.setFullYear(2021,5,3);
var d1 = new Date();
d1.setFullYear(year,month,day);
var diff = d1 - d0;
diff = diff/1000/60/60/24
if (minute < 10){
    document.getElementById("time").innerHTML = "D"+diff+" "+hour+":0"+minute;
}
else{
    document.getElementById("time").innerHTML = "D"+diff+" "+hour+":"+minute;
}