//加载页面时更新
function load_updata()
{
    //获取日期，天气
    load_date();
    //如果登录了，跳转到主页
    if (is_login() == 1)
    {
        window.location.href = "index.html";
    }
}

window.onload = load_updata;