
function load_siwei()
{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange= function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            load_siwei2(this)
		}
	}
    xmlhttp.open("GET","http://127.0.0.1:8000/siwei/",true);
    xmlhttp.send();
}

function load_siwei2(xml)
{
    var str = xml.responseText;
    var json_str = JSON.parse(str);
    var happy = Number(json_str["data"]["happy"]);
    document.getElementById("happy").innerHTML = happy;
}
//加载页面时更新
function load_updata()
{
    load_siwei()
}

window.onload = load_updata;