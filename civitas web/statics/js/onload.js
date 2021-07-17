//加载页面时更新
function load_updata()
{
    //获取状态值
    var value = getvalue();
    var stamina_value = value["stamina_value"];
    var happiness_value = value["happiness_value"];
    var health_value = value["health_value"];
    var starvation_value = value["starvation_value"];
    //更新状态值
    updata(stamina_value,happiness_value,health_value,starvation_value);
    //获取演讲
    load_speech(1);
}

window.onload = load_updata;