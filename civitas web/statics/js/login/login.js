function is_login()
{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText
            var json_str = JSON.parse(str);
            return str
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/islogin/",true);
    xmlhttp.withCredentials = true;
    xmlhttp.send();
}

function login()
{
    var account = document.getElementById("account").value;
    var password = document.getElementById("password").value;
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText
            var json_str = JSON.parse(str);
            if (json_str["message"] != "登录成功")
            {
                document.getElementById("message").innerHTML = json_str["message"];
                //document.getElementById("account").value = "";
                //document.getElementById("password").value = "";
            }
            else
            {
                window.location.href = "index.html";
            }
		}
	}
    xmlhttp.open("POST","https://api.trickydeath.xyz/login/",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.withCredentials = true;
    xmlhttp.send("username="+account+"&password="+password);
}