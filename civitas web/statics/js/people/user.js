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
            document.getElementById("main").innerHTML = "<p class=\"main-char\">该用户不存在！</p>"
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
        document.getElementById("avatar").innerHTML = `
            <div class="main-people">
                <img src="https://api.trickydeath.xyz/getavatar/?uid=`+uid+`" class="img-thumbnail" width="100px" height="100px"/>
                <div class="main-people-text">
                    <p>`+json_str["data"]["username"]+`</p>
                    <p class="author">>位于京兆尹，长安县 >籍贯京兆尹</p>
                    <p class="author">><a href="?uid=`+uid+`">`+json_str["data"]["username"]+`库房</a></p>
                </div>
            </div>`;
    }
    xmlhttp.open("GET","https://api.trickydeath.xyz/getuserdetail/?uid=" + uid,true);
    xmlhttp.withCredentials = true;
    xmlhttp.send();
}