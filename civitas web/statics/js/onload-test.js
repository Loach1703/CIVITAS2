
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
    var elem_happy = document.getElementById("happiness");
    var width_happy = happy;

    var energy = Number(json_str["data"]["energy"]);
    var elem_energy = document.getElementById("happiness");
    var width_energy = energy;

    var healthy = Number(json_str["data"]["healthy"]);
    var elem_healthy = document.getElementById("happiness");
    var width_healthy = healthy;

    var hunger = Number(json_str["data"]["hunger"]);
    var elem_hunger = document.getElementById("happiness");
    var width_hunger = hunger;
    
    elem_energy.style.width = width_energy + '%';
    document.getElementById("label_energy").innerHTML = '精力 '+ width_happy * 1 + '/100';

    elem_happy.style.width = width_happy + '%';
    document.getElementById("label_happy").innerHTML = '快乐 '+ width_happy * 1 + '/100';

    elem_healthy.style.width = width_healthy + '%';
    document.getElementById("label_healthy").innerHTML = '健康 '+ width_happy * 1 + '/100';

    elem_happy.style.width = width_hunger + '%';
    document.getElementById("label_hunger").innerHTML = '饥饿 '+ width_hunger * 1 + '/100';





    
    
    
}
//加载页面时更新
function load_updata()
{
    load_siwei()
}

window.onload = load_updata;