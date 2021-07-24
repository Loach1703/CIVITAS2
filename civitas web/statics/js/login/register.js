function register()
{
    var account = document.getElementById("account").value;
    var password = document.getElementById("password").value;
    var repeat_password = document.getElementById("repeat-password").value;
    var email = document.getElementById("email").value;
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText
            var json_str = JSON.parse(str);
            if (json_str["message"] != "注册成功")
            {
                document.getElementById("message").innerHTML = json_str["message"];
            }
            else
            {
                login(account,password)
                window.location.href = "index.html";
            }
		}
	}
    xmlhttp.open("POST","https://api.trickydeath.xyz/register/",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    //xmlhttp.withCredentials = true;
    xmlhttp.send("username="+account+"&password="+password+"&repeat_password="+repeat_password+"&email="+email);
}