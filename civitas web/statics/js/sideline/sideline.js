/*
副业
do_sideline：进行副业
*/

function do_sideline(sideline_id)
{
    /*参数说明：
    sideline_id：副业编号
    */
    if (isNaN(sideline_id))
    {
        return;
    }
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function()
    {
        var str = xmlhttp.responseText;
        var json_str = JSON.parse(str);
    }
    xmlhttp.open("POST","https://api.trickydeath.xyz/dosideline/",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.withCredentials = true;
    xmlhttp.send("sidelineid="+sideline_id);
}