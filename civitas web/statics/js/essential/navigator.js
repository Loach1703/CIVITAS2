/*
导航栏
navigator：根据是否登录，写入不同的导航栏
date_navigator：获取日期，显示在导航栏上
left_navigator：显示左侧导航栏
*/

function navigator(status,uid)
{
    /*参数说明：
    status：登录状态，由is_login函数返回值得到
    uid：用户id
    */
    if (uid == null)
    {
        uid = 0;
    }
    var nav = document.getElementById("navigator");
    //已登录
    if (status == 1)
    {
        nav.innerHTML = `
            <img src="civitas/img/CIVITAS2.png" width="120px" height="25px" class="civitas2"/>
            <span class="vertime">Pre-Alpha 0.0.10
                <p id="time" class="time"></p>
            </span>
            <span>
                <a href="#street"><img src="civitas/svg/common/street.svg" width="22px" height="22px"/>城市</a>
                <a href="map.html"><img src="civitas/svg/common/map.svg" width="22px" height="22px"/>地图</a>
            </span>
            <span class="market-main" id="market">
                <a href="#market"><img src="civitas/svg/common/market.svg" width="22px" height="22px"/>市场</a>
                <div id="market-down" class="market-dropdown hide">
                    <a href="#square"><img src="civitas/svg/common/goods.svg" width="22px" height="22px"/>物资市场</a>
                    <a href="#square"><img src="civitas/svg/common/recruit.svg" width="22px" height="22px">招聘市场</a>
                    <a href="#square"><img src="civitas/svg/common/estate.svg" width="22px" height="22px"/>不动产市场</a>
                </div>
            </span>
            <span>
                <a href="blog/1.html"><img src="civitas/svg/common/blog.svg" width="22px" height="22px"/>开发日志</a>
            </span>
            <span class="signup-in">
                <img src="https://api.trickydeath.xyz/getavatar/?uid=`+uid+`" width="40px" height="40px"/>
                <a href="javascript:void(0)" onclick="log_out()">注销</a>
            </span>`
    }
    else
    {
        nav.innerHTML = `
            <img src="civitas/img/CIVITAS2.png" width="120px" height="25px" class="civitas2"/>
            <span class="vertime">Pre-Alpha 0.0.10
                <p id="time" class="time"></p>
            </span>
            <span>
                <a href="blog/1.html"><img src="civitas/svg/common/blog.svg" width="22px" height="22px"/>开发日志</a>
            </span>
            <span class="signup-in">
                <a href="login.html">登录</a>
                <a href="register.html">注册</a>
            </span>`
    }
    date_navigator();
}

function date_navigator()
{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange= function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText;
            var json_str = JSON.parse(str);
            var total_day = json_str["data"]["total_day"];
            var season = json_str["data"]["season"];
            var time = json_str["data"]["time"];
            var year = json_str["data"]["year"];
            var reg = /\d{2}/g;
            var time2 = time.match(reg);
            var hour = time2[0];
            var minute = time2[1];
            document.getElementById("time").innerHTML = "Y"+year+" "+season+" D"+total_day+" "+hour+":"+minute;
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/getdate/",true);
    xmlhttp.send();
}