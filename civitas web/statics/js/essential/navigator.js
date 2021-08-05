/*
导航栏
navigator：根据是否登录，写入不同的导航栏
date：获取日期，显示在导航栏上
left_navigator：显示左侧导航栏
status_left_navigator：显示左侧导航栏的用户状态
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
        nav.innerHTML = "<img src=\"civitas/img/CIVITAS2.png\" width=\"120px\" height=\"25px\" class=\"civitas2\"/><span class=\"vertime\">Pre-Alpha 0.0.6<p id=\"time\" class=\"time\"></p></span><span><a href=\"#street\"><img src=\"\
            civitas/svg/common/street.svg\" width=\"22px\" height=\"22px\"/>县城</a><a href=\"map.html\"><img src=\"civitas/svg/common/map.svg\" width=\"22px\" height=\"22px\"/>地图</a></span><span class=\"market-main\" id=\"market\"><a \
            href=\"#market\"><img src=\"civitas/svg/common/market.svg\" width=\"22px\" height=\"22px\"></img>市场</a><div id=\"market-down\" class=\"market-dropdown hide\"><a href=\"#square\"><img src=\"civitas/svg/common/goods.svg\" \
            width=\"22px\" height=\"22px\"></img>物资市场</a><a href=\"#square\"><img src=\"civitas/svg/common/recruit.svg\" width=\"22px\" height=\"22px\"></img>招聘市场</a><a href=\"#square\"><img src=\"civitas/svg/common/estate.svg\" \
            width=\"22px\" height=\"22px\"></img>不动产市场</a></div></span><span><a href=\"blog/1.html\"><img src=\"civitas/svg/common/blog.svg\" width=\"22px\" height=\"22px\"/>开发日志</a></span><span class=\"signup-in\"><img src=\"https://api.trickydeath.xyz/getavatar/?uid="+uid+"\" width=\"40px\" height=\"40px\"/><a  href=\"javascript:void(0)\" onclick=\"log_out()\">注销</a></span>"
    }
    else
    {
        nav.innerHTML = "<img src=\"civitas/img/CIVITAS2.png\" width=\"120px\" height=\"25px\" class=\"civitas2\"/><span class=\"vertime\">Pre-Alpha 0.0.6<p id=\"time\" class=\"time\"></p></span><span><a href=\"blog/1.html\"><img src=\"civitas/svg/common/blog.svg\" width=\"22px\" height=\"22px\"/>开发日志</a></span><span class=\"signup-in\"><a href=\"login.html\">登录</a><a href=\"register.html\">注册</a></span>"
    }
    date();
}

function date()
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
            var reg = /\d{2}/g;
            var time2 = time.match(reg);
            var hour = time2[0];
            var minute = time2[1];
            document.getElementById("time").innerHTML = season+" D"+total_day+" "+hour+":"+minute;
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/getdate/",true);
    xmlhttp.send();
}

function left_navigator(username,uid)
{
    /*参数说明：
    username：用户名
    uid：用户id
    */
    if (uid == null)
    {
        uid = 0;
    }
    var nav = document.getElementById("left-navigator");
    nav.innerHTML = "<div class=\"bottomline\"><span class=\"avatar\"><img src=\"https://api.trickydeath.xyz/getavatar/?uid="+uid+"\" class=\"img-thumbnail\" width=\"80px\" height=\"80px\"/></span><div class=\"level\"><a href=\"people.html?uid="+uid+"\" id=\"username\">"+username+"</a><p>等级 100级</p><div class=\"progress levelbar\"><div class=\"progress-bar bg-warning progress-bar-striped progress-bar-animated\" style=\"width: 50%\" id=\"energy\"><p class=\"xp\">经验 1000 / 2000</p></div></div></div></div><div class=\"bottomline\"><p class=\"menu\">我的状态</p><div id=\"status\"></div></div><div class=\"left-navigator-option\"><div class=\"bottomline\"><p class=\"menu\">我的CIVITAS</p><a href=\"index.html\">我的CIVITAS</a><a href=\"#news\">我的通知</a><a href=\"settings.html\">我的设置</a></div><div class=\"bottomline\"><p class=\"menu\">我的生活</p><a href=\"#home\">我的食谱</a><a href=\"#home\">我的藏书</a><a href=\"#news\">我的副业</a><a href=\"#news\">我的教育</a></div><div class=\"bottomline\"><p class=\"menu\">我的交际圈</p><a href=\"#home\">我的人际关系</a><a href=\"#news\">我的社交活动</a></div><div class=\"bottomline\"><p class=\"menu\">我的资产</p><a href=\"#home\">我的库房</a><a href=\"#news\">我的私人交易</a><a href=\"#news\">我管理的不动产</a><a href=\"#home\">我拥有的不动产</a></div></div>";
    status_left_navigator();
}

function status_left_navigator()
{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange= function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText;
            var json_str = JSON.parse(str);
            var status_data = json_str["data"];
            var stamina = status_data["today"]["stamina"];
            var happiness = status_data["today"]["happiness"];
            var health = status_data["today"]["health"];
            var starvation = status_data["today"]["starvation"];
            var status_html = document.getElementById("status");
            var status_dict = {};
            //状态对应颜色
            if (stamina < 20)
            {
                status_dict["stamina"] = "progress-bar progress-bar-striped progress-bar-animated bg-danger";
            }
            else if (stamina < 40)
            {
                status_dict["stamina"] = "progress-bar progress-bar-striped progress-bar-animated bg-warning";
            }
            else if (stamina < 60)
            {
                status_dict["stamina"] = "progress-bar progress-bar-striped progress-bar-animated bg-success";
            }
            else if (stamina < 80)
            {
                status_dict["stamina"] = "progress-bar progress-bar-striped progress-bar-animated bg-info";
            }
            else if (stamina <= 100)
            {
                status_dict["stamina"] = "progress-bar progress-bar-striped progress-bar-animated";
            }
            if (happiness < 20)
            {
                status_dict["happiness"] = "progress-bar progress-bar-striped progress-bar-animated bg-danger";
            }
            else if (happiness < 40)
            {
                status_dict["happiness"] = "progress-bar progress-bar-striped progress-bar-animated bg-warning";
            }
            else if (happiness < 60)
            {
                status_dict["happiness"] = "progress-bar progress-bar-striped progress-bar-animated bg-success";
            }
            else if (happiness < 80)
            {
                status_dict["happiness"] = "progress-bar progress-bar-striped progress-bar-animated bg-info";
            }
            else if (happiness <= 100)
            {
                status_dict["happiness"] = "progress-bar progress-bar-striped progress-bar-animated";
            }
            if (health < 20)
            {
                status_dict["health"] = "progress-bar progress-bar-striped progress-bar-animated bg-danger";
            }
            else if (health < 40)
            {
                status_dict["health"] = "progress-bar progress-bar-striped progress-bar-animated bg-warning";
            }
            else if (health < 60)
            {
                status_dict["health"] = "progress-bar progress-bar-striped progress-bar-animated bg-success";
            }
            else if (health < 80)
            {
                status_dict["health"] = "progress-bar progress-bar-striped progress-bar-animated bg-info";
            }
            else if (health <= 100)
            {
                status_dict["health"] = "progress-bar progress-bar-striped progress-bar-animated";
            }
            if (starvation < 20)
            {
                status_dict["starvation"] = "progress-bar progress-bar-striped progress-bar-animated bg-danger";
            }
            else if (starvation < 40)
            {
                status_dict["starvation"] = "progress-bar progress-bar-striped progress-bar-animated bg-warning";
            }
            else if (starvation < 60)
            {
                status_dict["starvation"] = "progress-bar progress-bar-striped progress-bar-animated bg-success";
            }
            else if (starvation < 80)
            {
                status_dict["starvation"] = "progress-bar progress-bar-striped progress-bar-animated bg-info";
            }
            else if (starvation <= 100)
            {
                status_dict["starvation"] = "progress-bar progress-bar-striped progress-bar-animated";
            }
            //换日回复值
            var stamina_change = status_data["tomorrow"]["stamina_change"];
            var happiness_change = status_data["tomorrow"]["happiness_change"];
            var health_change = status_data["tomorrow"]["health_change"];
            var starvation_change = status_data["tomorrow"]["starvation_change"];
            if (stamina_change < 0)
            {
                stamina_change = " - " + Math.abs(stamina_change).toFixed(1);
            }
            else if(stamina_change >= 0)
            {
                stamina_change = " + " + stamina_change.toFixed(1);
            }
            if (happiness_change < 0)
            {
                happiness_change = " - " + Math.abs(happiness_change).toFixed(1);
            }
            else if(happiness_change >= 0)
            {
                happiness_change = " + " + happiness_change.toFixed(1);
            }
            if (health_change < 0)
            {
                health_change = " - " + Math.abs(health_change).toFixed(1);
            }
            else if(health_change >= 0)
            {
                health_change = " + " + health_change.toFixed(1);
            }
            if (starvation_change < 0)
            {
                starvation_change = " - " + Math.abs(starvation_change).toFixed(1);
            }
            else if(starvation_change >= 0)
            {
                starvation_change = " + " + starvation_change.toFixed(1);
            }
            status_html.innerHTML = "<div class=\"progress status\"><div class=\""
            +status_dict["stamina"]+"\" style=\"width: "+stamina+"%\">精力 "+stamina+" / 100"
            +stamina_change+"</div></div><div class=\"progress status\"><div class=\""
            +status_dict["happiness"]+"\" style=\"width: "+happiness+"%\">快乐 "+happiness+" / 100"
            +happiness_change+"</div></div><div class=\"progress status\"><div class=\""
            +status_dict["health"]+"\" style=\"width: "+health+"%\">健康 "+health+" / 100"
            +health_change+"</div></div><div class=\"progress status\"><div class=\""
            +status_dict["starvation"]+"\" style=\"width: "+starvation+"%\">饥饿 "+starvation+" / 100"
            +starvation_change+"</div></div>"
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/getstatus/",true);
    xmlhttp.withCredentials = true;
    xmlhttp.send();
}

/*
html源代码
登录
<nav class="navigator">
    <img src="civitas/img/CIVITAS2.png" width="120px" height="25px" class="civitas2"/>
    <span class="vertime">
        Pre-Alpha 0.0.5
        <p id="time" class="time"></p>
    </span>
    <span>
        <a href="#street"><img src="civitas/svg/common/street.svg" width="22px" height="22px"/>县城</a>
        <a href="map.html"><img src="civitas/svg/common/map.svg" width="22px" height="22px"/>地图</a>
    </span>
    <span class="market-main" id="market">
        <a href="#market"><img src="civitas/svg/common/market.svg" width="22px" height="22px"></img>市场</a>
        <div id="market-down" class="market-dropdown hide">
            <a href="#square"><img src="civitas/svg/common/goods.svg" width="22px" height="22px"></img>物资市场</a>
            <a href="#square"><img src="civitas/svg/common/recruit.svg" width="22px" height="22px"></img>招聘市场</a>
            <a href="#square"><img src="civitas/svg/common/estate.svg" width="22px" height="22px"></img>不动产市场</a>
        </div>
    </span>
    <span>
      <a href="blog/1.html"><img src="civitas/svg/common/blog.svg" width="22px" height="22px"/>开发日志</a>
    </span>
    <span class="signup-in">
        <img src="civitas/img/1.png" width="40px" height="40px"/>
        <a href="javascript:void(0)" onclick="log_out()">注销</a>
    </span>
</nav>

未登录
<nav class="navigator">
    <img src="civitas/img/CIVITAS2.png" width="120px" height="25px" class="civitas2"/>
    <span class="vertime">
        Pre-Alpha 0.0.5
        <p id="time" class="time"></p>
    </span>
    <span>
      <a href="blog/1.html"><img src="civitas/svg/common/blog.svg" width="22px" height="22px"/>开发日志</a>
    </span>
    <span class="signup-in">
        <a href="login.html">登录</a>
        <a href="register.html">注册</a>
    </span>
</nav>

左侧导航栏
<div class="bottomline">
    <span class="avatar">
        <img src="civitas/img/1.png" class="img-thumbnail" width="80px" height="80px"/>
    </span>
    <div class="level">
        <a href="#" id="username"></a>
        <p>等级 100级</p>
        <div class="progress levelbar">
            <div class="progress-bar bg-warning progress-bar-striped progress-bar-animated"  style="width: 50%" id="energy"><p class="xp">经验 1000 / 2000</p></div>
        </div>
    </div>
</div>
<div class="bottomline" id="status">
</div>
<div class="left-navigator-option">
    <div class="bottomline">
        <p class="menu">我的CIVITAS</p>
        <a href="index.html">我的CIVITAS</a>
        <a href="#news">我的通知</a>
        <a href="#news">我的设置</a>
    </div>
    <div class="bottomline">
        <p class="menu">我的生活</p>
        <a href="#home">我的食谱</a>
        <a href="#home">我的藏书</a>
        <a href="#news">我的副业</a>
        <a href="#news">我的教育</a>
    </div>
    <div class="bottomline">
        <p class="menu">我的交际圈</p>
        <a href="#home">我的人际关系</a>
        <a href="#news">我的社交活动</a>
    </div>
    <div class="bottomline">
        <p class="menu">我的资产</p>
        <a href="#home">我的库房</a>
        <a href="#news">我的私人交易</a>
        <a href="#news">我管理的不动产</a>
        <a href="#home">我拥有的不动产</a>
    </div>
</div>
*/