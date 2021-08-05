/*
技能相关
load_skill：加载技能
*/

function load_skill(uid=null)
{
    /*参数说明：
    uid：需要读取技能的用户uid
    额外说明：这个函数是主页/个人主页通用的，所以需要一个判别的uid，在主页使用时，不需要加uid，api会返回当前登录cookie对应用户的技能
    */
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var i;
            var str = xmlhttp.responseText;
            var json_str = JSON.parse(str);
            var skill_html = document.getElementById("skill");
            var skill_inner = "";
            var skill_data = json_str["data"];
            var skill_dict = {1:"学徒",2:"匠人",3:"匠师",4:"专家",5:"大师",6:"宗师",7:"大宗师"}
            if (uid == null)
            {
                skill_html.innerHTML = "<p class=\"main-char\">我的技能</p>";
            }
            else
            {
                skill_html.innerHTML = "<p class=\"main-char\">他的技能</p>";
            }
            for (i = 0; i < skill_data.length ; i++)
            {
                var skill_data_detail = skill_data[i];
                var skill_id = skill_data_detail["id"];
                var level = skill_data_detail["level"];
                var skill_num = skill_data_detail["skill"].toFixed(2);
                if (skill_num == 0)
                {
                    continue;
                }
                skill_inner += "<div class=\"skill-box\"><div class=\"skill-picture\"><img src=\"civitas/icon/skill/"
                +skill_id+"/s.png\" width=\"80px\" height=\"80px\"/></div><div class=\"skill-name\"><p class=\"skill-name-left\">"
                +skill_data_detail["name"]+"</p><p class=\"skill-name-right skill-name-right"+level+"\">"+skill_dict[level]+" "
                +skill_num+"</p></div>";
                var j;
                var skill_mini_list = skill_data_detail["list"];
                var skill_mini_inner = "";
                for (j = 0; j < skill_mini_list.length ; j++)
                {
                    var skill_mini_data_detail = skill_mini_list[j];
                    var skill_mini_id = skill_mini_data_detail["id"];
                    var skill_mini_num = (skill_mini_data_detail["skill"] * 100).toFixed(1);
                    if (skill_mini_num == 0)
                    {
                        continue
                    }
                    skill_mini_inner += "<div class=\"skill-mini\"><img src=\"civitas/icon/skill/"
                    +skill_id+"/"+skill_mini_id+".png\" width=\"40px\" height=\"40px\"/><p>"
                    +skill_mini_data_detail["name"]+" "+skill_mini_num+"%</p></div>"
                }
                if (skill_mini_inner == "")
                {
                    skill_mini_inner += "<div class=\"skill-mini-div-none\">";
                }
                else
                {
                    skill_mini_inner = "<div class=\"skill-mini-div\">" + skill_mini_inner;
                }
                skill_inner += skill_mini_inner
                skill_inner += "</div></div>"
            }
            if (skill_inner == "")
            {
                if (uid == null)
                {
                    skill_inner = "<div class=\"skill-name\"><p class=\"skill-name-left\">您还没有技能，去工作或是演讲，副业以获得技能。</p></div>"
                }
                else
                {
                    skill_inner = "<div class=\"skill-name\"><p class=\"skill-name-left\">他还没有技能。</p></div>"
                }
            }
            skill_html.innerHTML += skill_inner
		}
	}
    if (uid == null)
    {
        xmlhttp.open("GET","https://api.trickydeath.xyz/getskill/",true);
    }
    else
    {
        xmlhttp.open("GET","https://api.trickydeath.xyz/getskill/?uid=" + uid,true);
    }
    xmlhttp.withCredentials = true;
    xmlhttp.send();
}

/*
<p class="main-char">我的技能</p>
    <div class="skill-box">
        <div class="skill-picture">
            <img src="civitas/icon/skill/1/s.png" width="80px" height="80px"/>
        </div>
        <div class="skill-name">
            <p class="skill-name-left">耕作</p>
            <p class="skill-name-right skill-name-right7">大宗师 12.34</p>
        </div>
        <div class="skill-mini-div">
            <div class="skill-mini">
                <img src="civitas/icon/skill/1/1.png" width="40px" height="40px"/>
                <p>粮食种植 45%</p>
            </div>
            <div class="skill-mini">
                <img src="civitas/icon/skill/1/2.png" width="40px" height="40px"/>
                <p>蔬果种植 45%</p>
            </div>
            <div class="skill-mini">
                <img src="civitas/icon/skill/1/3.png" width="40px" height="40px"/>
                <p>经济作物种植 45% </p>
            </div>
            <div class="skill-mini">
                <img src="civitas/icon/skill/1/4.png" width="40px" height="40px"/>
                <p>开垦 45% </p>
            </div>
        </div>
    </div>
*/