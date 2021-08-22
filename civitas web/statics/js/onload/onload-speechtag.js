/*
演讲话题页面使用的加载
load_updata：读取页面
*/

function load_updata()
{
    //获得是否登录接口返回值
    var json_str_login = is_login();
    //重定向
    redirection(json_str_login["status"]);
    //获取导航栏
    navigator(json_str_login["status"],json_str_login["data"]["uid"]);
    left_navigator(json_str_login["data"]["uid"]);
    //找不到参数，重定向至主页
    if (isNaN(get_parameter_value("tagid")))
    {
        window.location.href = "index.html";
        return;
    }
    //获取指定话题的演讲
    load_speech(1,null,get_parameter_value("tagid"));
}

window.onload = load_updata;