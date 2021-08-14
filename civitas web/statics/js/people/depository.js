/*
获取库房信息
load_depository：获得库房信息
*/

function load_depository(uid)
{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange= function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText;
            var json_str = JSON.parse(str);
            var json_data = json_str["data"];
            var material_html = "";
            if (json_str["status"] == 0)
            {
                document.getElementById("depository-name").innerHTML = "找不到该用户！"
                return;
            }
            for (var i=0; i<json_data.length; i++)
            {
                var material_data = json_data[i];
                material_html += "<div class=\"depository-box bottomline-dashed\"><img src=\"civitas/icon/goods/"
                +material_data["id"]+".png\" width=\"60px\" height=\"60px\" class=\"depository-mainimg\"/><span class=\"depository-text1\"><p class=\"depository-name\">"
                +material_data["name"]+"<br></p><p class=\"depository-loss\">仓储损耗 "
                +material_data["wastage"]+"</p></span><span class=\"depository-text2\"><p class=\"depository-num\">"
                +material_data["total"].toFixed(2)+"<br></p><p class=\"depository-loss\">总量</p></span><span class=\"depository-text2\"><p class=\"depository-num\">"
                +(material_data["total"]*material_data["unitmass"]).toFixed(2)+"<br></p><p class=\"depository-loss\">每单位重量 "
                +material_data["unitmass"]+"</p></span></div>"
            }
            if (material_html != "") 
            {
                material_html = "<div class=\"depository-box-top bottomline-dashed\"><span class=\"depository-text-top\"><p class=\"depository-name\">物品名</p></span><span class=\"depository-text2\"><p class=\"depository-num\">总数量</p></span><span class=\"depository-text2\"><p class=\"depository-num\">总质量</p></span></div>" + material_html;
                document.getElementById("depository-detail").innerHTML = material_html;
            }
            else
            {
                document.getElementById("depository-detail").innerHTML = "<div class=\"depository-box\"><p id=\"depository-none\" class=\"depository-name\"></p></div>";
            }
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/getmaterial/?uid=" + uid,true);
    xmlhttp.withCredentials = true;
    xmlhttp.send();
    var xmlhttp2 = new XMLHttpRequest();
    xmlhttp2.onreadystatechange = function()
    {
        var str = xmlhttp2.responseText;
        var json_str = JSON.parse(str);
        document.title = json_str["data"]["username"]+"的库房 - 古典社会模拟 CIVITAS2";
        document.getElementById("depository-name").innerHTML = json_str["data"]["username"]+"的库房";
        try
        {
            document.getElementById("depository-none").innerHTML = json_str["data"]["username"]+"还没有物品。";
        }
        catch (e){}
    }
    xmlhttp2.open("GET","https://api.trickydeath.xyz/getuserdetail/?uid=" + uid,true);
    xmlhttp2.withCredentials = true;
    xmlhttp2.send();
}

/*
<div class="depository-box bottomline-dashed">
    <img src="civitas/icon/goods/1.png" width="60px" height="60px" class="depository-mainimg"/>
    <span class="depository-text1">
        <p class="depository-name">小麦<br></p>
        <p class="depository-loss">仓储损耗 10%</p>
    </span>
    <span class="depository-text2">
        <p class="depository-num">100<br></p>
        <p class="depository-loss">总量</p>
    </span>
    <span class="depository-text2">
        <p class="depository-num">100<br></p>
        <p class="depository-loss">每单位重量 1.00</p>
    </span>
</div>
*/