function is_login()
{
    var xmlhttp = new XMLHttpRequest();
    var json_str;
    xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText;
            json_str = JSON.parse(str);
            document.getElementById("username").innerHTML = json_str["data"]["username"];
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/islogin/",false);
    xmlhttp.withCredentials = true;
    xmlhttp.send();
    return json_str["message"];
}