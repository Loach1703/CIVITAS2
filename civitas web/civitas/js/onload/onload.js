function load_updata() {
    //获得是否登录接口返回值
    var json_str_login = is_login();
    //重定向
    redirection(json_str_login.status);
    //加载Vue
    load_main_vm(json_str_login.status,json_str_login.data.uid);
}

window.onload = load_updata;