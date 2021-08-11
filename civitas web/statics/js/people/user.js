/*
获得用户详细信息，在个人主页使用
load_user_detail：获得用户详细信息
*/

function load_user_detail(uid)
{
    /*参数说明：
    uid：用户id
    */
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function()
    {
        var str = xmlhttp.responseText;
        var json_str = JSON.parse(str);
        if (json_str["status"] == 0)
        {
            document.title = "个人主页 - 古典社会模拟 CIVITAS2";
            document.getElementById("main").innerHTML = "<h1>该用户不存在！</h1>"
            return
        }
        document.title = json_str["data"]["username"]+"的主页 - 古典社会模拟 CIVITAS2";
        document.getElementById("speech-username").innerHTML = json_str["data"]["username"]+"的演讲"
        document.getElementById("skill-username").innerHTML = json_str["data"]["username"]+"的技能"
        try
        {
            document.getElementById("skill-none").innerHTML = json_str["data"]["username"]+"还没有技能"
        }
        catch(e){}
        document.getElementById("avatar").innerHTML = "<p class=\" main-subchar\"><img src=\"https://api.trickydeath.xyz/getavatar/?uid="
            +uid+"\" class=\"img-thumbnail\" width=\"100px\" height=\"100px\"/>"
            +json_str["data"]["username"]+"</p>";
    }
    xmlhttp.open("GET","https://api.trickydeath.xyz/getuserdetail/?uid=" + uid,true);
    xmlhttp.withCredentials = true;
    xmlhttp.send();
}