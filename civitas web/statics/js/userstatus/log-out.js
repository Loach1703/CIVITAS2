/*
注销
log_out：注销
*/

function log_out()
{
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText;
            var json_str = JSON.parse(str);
            if (json_str["status"] == 1)
            {
                window.location.href = "login.html";
            } 
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/logout/",true);
    xmlhttp.withCredentials = true;
    xmlhttp.send();
}