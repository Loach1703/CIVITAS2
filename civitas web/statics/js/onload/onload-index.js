/*
主页使用的加载，包括加载天气，技能，演讲等
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
    left_navigator(json_str_login["data"]["username"],json_str_login["data"]["uid"]);
    //获取天气
    load_weather();
    //获取演讲
    load_speech(1);
    popular_speech();
}

window.onload = load_updata;