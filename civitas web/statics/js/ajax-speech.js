function load_speech(page)
{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange= function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            load_speech2(this,page)
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/getspeech/?page=" + page,true);
    xmlhttp.send();
}

function load_speech2(xml,page)
{
    var i;
    var str = xml.responseText;
    var json_str = JSON.parse(str);
    var total_page = json_str["data"]["total_page"]
    var speech="";
    var speech_paginator="";
    //显示演讲
    for (i = 0; i <= json_str["data"]["num"]-1; i++)
    { 
        speech += "<div class=\"speech\"><img src=\"civitas/img/1.png\" class=\"img-thumbnail speech-avatar\" width=\"50px\" height=\"50px\"\
            /><span class=\"speech-content\"><a href=\"#\" class=\"speech-name\">CIVITAS2团队</a><p>："
            +json_str["data"]["datalist"][i]["text"]+"</p></span><div class=\"speech-bottom\"><p>本地演讲，第"
            +json_str["data"]["datalist"][i]["day"]+"天，"+json_str["data"]["datalist"][i]["time"]+
            "</p></div><div class=\"speech-bottom\"><a href=\"#\">欢呼(0) </a><a href=\"#\">关注(0) </a><a href=\"#\">倒彩(0)</a></div></div>";
    }
    //小于等于7页演讲，直接显示所有页数
    if (total_page <= 7)
    {
        for (i = 1; i <= total_page; i++)
        {
            if (i == page)
            {
                speech_paginator += "<span class=\"thispage\">"+i+"</span>";
            }
            else
            {
                speech_paginator += "<a href=\"javascript:void(0)\" onclick=\"load_speech("+i+")\">"+i+"</a>";
            }
        }
    }
    //大于7页，显示省略符
    //跳转
    speech_paginator += "<div class=\"input-group input-group-sm\"><input type=\"text\" class=\"form-control speech-page-swap-input\" \
        id=\"speech-page-swap-input\" placeholder=\"跳转到某页\"><button type=\"submit\" class=\"btn btn-primary speech-page-swap-button\" \
        onclick=\"speech_swap()\">跳转</button></div>"
    document.getElementById("speech-page-paginator").innerHTML = speech_paginator;
    document.getElementById("speech").innerHTML = speech;
}

function speech_swap()
{
    var page = document.getElementById("speech-page-swap-input").value;
    load_speech(page)
}

/*
"<div class=\"speech\">
    <img src=\"civitas/img/1.png\" class=\"img-thumbnail speech-avatar\" width=\"50px\" height=\"50px\"/>
    <span class=\"speech-content\">
        <a href=\"#\" class=\"speech-name\">CIVITAS2团队</a>
        <p>："+json_str["data"]["datalist"][i]["text"]+"</p>
    </span>
    <div class=\"speech-bottom\">
        <p>本地演讲，第"+json_str["data"]["datalist"][i]["day"]+"天，"+json_str["data"]["datalist"][i]["time"]+"</p>
    </div>
    <div class=\"speech-bottom\">
        <a href=\"#\">欢呼(0) </a>
        <a href=\"#\">关注(0) </a>
        <a href=\"#\">倒彩(0)</a>
    </div>
</div>"

<span class="thispage">1</span>
<a onclick="">2</a>
<a href="?start=60">3</a>
<a href="?start=90">4</a>
<a href="?start=120">5</a>
<span class="break">...</span>
<a href="?start=9570">320</a>
<a href="?start=9600">321</a>
<div class="input-group input-group-sm">
    <input type="text" class="form-control speech-page-swap-input" id="speech-page-swap-input" placeholder="跳转到某页">
    <button type="submit" class="btn btn-primary speech-page-swap-button" onclick="">跳转</button>
</div>
*/