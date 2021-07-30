/*
判断是否登录
is_login：判断是否登录，返回接口提供的整个json
*/

function is_login()
{
    var xmlhttp = new XMLHttpRequest();
    var json_str_login;
    xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText;
            json_str_login = JSON.parse(str);
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/islogin/",false);
    xmlhttp.withCredentials = true;
    xmlhttp.send();
    return json_str_login;
}