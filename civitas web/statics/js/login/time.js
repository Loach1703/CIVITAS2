//从接口获取日期等
function load_date()
{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange= function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            load_date2(this)
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/getdate/",true);
    xmlhttp.send();
}

function load_date2(xml)
{
    var str = xml.responseText;
    var json_str = JSON.parse(str);
    var total_day = json_str["data"]["total_day"];
    var season = json_str["data"]["season"];
    var time = json_str["data"]["time"];
    var reg = /\d{2}/g;
    var time2 = time.match(reg);
    var hour = time2[0];
    var minute = time2[1];
    document.getElementById("time").innerHTML = season+" D"+total_day+" "+hour+":"+minute;
}