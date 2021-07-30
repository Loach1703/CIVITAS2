/*
未注册页面通用的加载
load_updata：读取页面
*/

function load_updata()
{
    //获得是否登录接口返回值
    var json_str_login = is_login();
    //重定向
    redirection(json_str_login["status"]);
    //获取导航栏
    navigator(json_str_login["status"]);
}

window.onload = load_updata;