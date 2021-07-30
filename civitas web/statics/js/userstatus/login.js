/*
登录
login_getvalue：获取用户输入值
login：根据账号密码发送post请求登录
之所以要分开，是因为注册后自动登录的需要
*/

function login_getvalue()
{
    var account = document.getElementById("account").value;
    var password = document.getElementById("password").value;
    login(account,password);
}


function login(account,password)
{
    /*参数说明：
    account：账号
    password：密码
    */
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText
            var json_str = JSON.parse(str);
            if (json_str["status"] != "1")
            {
                document.getElementById("message").innerHTML = json_str["message"];
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