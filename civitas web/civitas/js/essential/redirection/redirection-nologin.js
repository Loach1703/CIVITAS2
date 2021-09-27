function redirection(status)
{
    /*参数说明：
    status：登录状态，由is_login函数返回值得到
    */
    if (status == 1)
    {
        window.location.assign("index.html");
    }
}