function load_updata() {
    //获得是否登录接口返回值
    var json_str_login = is_login();
    //重定向
    redirection(json_str_login.status);
    //加载Vue
    load_main_vm(json_str_login.status,json_str_login.data.uid);
    //找不到参数，重定向至错误页面
    if (isNaN(get_parameter_value("id")) || get_parameter_value("id") == null) {
        window.location.assign("error.html");
    }
}

window.onload = load_updata;