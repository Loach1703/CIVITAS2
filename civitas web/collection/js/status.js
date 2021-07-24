//换日主函数
function day_change()
{
    //获取状态值，这些其实应该在后端的
    var value = getvalue();
    var stamina_value = value["stamina_value"];
    var happiness_value = value["happiness_value"];
    var health_value = value["health_value"];
    var starvation_value = value["starvation_value"];
    //换日属性变更计算
    var change = change_calc(stamina_value,happiness_value,health_value,starvation_value);
    var stamina_change = change["stamina_change"];
    var happiness_change = change["happiness_change"];
    var health_change = change["health_change"];
    var starvation_change = change["starvation_change"];
    //处理数据
    stamina_value += stamina_change;
    happiness_value += happiness_change;
    health_value += health_change;
    starvation_value -= starvation_change;
    //检查
    value = check(stamina_value,happiness_value,health_value,starvation_value);
    stamina_value = value["stamina_value"];
    happiness_value = value["happiness_value"];
    health_value = value["health_value"];
    starvation_value = value["starvation_value"];
    //精力最大值受健康最大值限制
    if (stamina_value > health_value)
    {
        stamina_value = health_value;
    }
    //更新
    updata(stamina_value,happiness_value,health_value,starvation_value);
    //返回在p区
    //var pget = document.getElementById("change");
    //pget.innerHTML = (stamina_change.toString()+"  "+happiness_change.toString()+"  "+health_change.toString()+"  "+starvation_change.toString());
}

//工作
function work(strategy)
{
    //获取状态值
    var value = getvalue();
    var stamina_value = value["stamina_value"];
    var happiness_value = value["happiness_value"];
    var health_value = value["health_value"];
    var starvation_value = value["starvation_value"];
    //工作变更基础
    var stamina_change = 25;
    var happiness_change = 3;
    var health_change = 3;
    var starvation_change = 3.5;
    //工作产能基础
    var capacity = 3
    //工作策略
    if (strategy == 1)
    {
        happiness_change *= 0.75;
        health_change *= 0.75;
    }
    else if (strategy == 2)
    {
        happiness_change *= 1;
        health_change *= 1;
    }
    else if (strategy == 3)
    {
        happiness_change *= 1.25;
        health_change *= 1.25;
    }
    else if (strategy == 4)
    {
        happiness_change *= 1.25;
        health_change *= 1.25;
    }
    else if (strategy == 5)
    {
        stamina_change *= 0.75;
        happiness_change *= 0.5;
        health_change *= 0.5;
        starvation_change *= 0.75;
    }
    //改变
    stamina_value -= stamina_change;
    happiness_value -= happiness_change;
    health_value -= health_change;
    starvation_value -= starvation_change;
    //检查
    value = check(stamina_value,happiness_value,health_value,starvation_value);
    stamina_value = value["stamina_value"];
    happiness_value = value["happiness_value"];
    health_value = value["health_value"];
    starvation_value = value["starvation_value"];
    //更新
    updata(stamina_value,happiness_value,health_value,starvation_value);
}

//吃饭
function eat()
{
    //获取状态值
    var value = getvalue();
    var stamina_value = value["stamina_value"];
    var happiness_value = value["happiness_value"];
    var health_value = value["health_value"];
    var starvation_value = value["starvation_value"];
    //吃饭变更值
    starvation_value += 11;
    //检查
    value = check(stamina_value,happiness_value,health_value,starvation_value);
    stamina_value = value["stamina_value"];
    happiness_value = value["happiness_value"];
    health_value = value["health_value"];
    starvation_value = value["starvation_value"];
    //更新
    updata(stamina_value,happiness_value,health_value,starvation_value);
}

//获得值
function getvalue()
{
    //获取状态值
    var stamina = document.getElementById("stamina");
    var happiness = document.getElementById("happiness");
    var health = document.getElementById("health");
    var starvation = document.getElementById("starvation");
    var reg = /\d{1,3}.\d|\d{1,3}/;
    var stamina_value = stamina.innerHTML.match(reg);
    var happiness_value = happiness.innerHTML.match(reg);
    var health_value = health.innerHTML.match(reg);
    var starvation_value = starvation.innerHTML.match(reg);
    //转型
    stamina_value = Number(stamina_value);
    happiness_value = Number(happiness_value);
    health_value = Number(health_value);
    starvation_value = Number(starvation_value);
    //以json形式返回
    var value={"stamina_value":stamina_value,"happiness_value":happiness_value,"health_value":health_value,"starvation_value":starvation_value};
    return value;
}

//更新数据
function updata(stamina_value,happiness_value,health_value,starvation_value)
{
    //获取id
    var stamina = document.getElementById("stamina");
    var happiness = document.getElementById("happiness");
    var health = document.getElementById("health");
    var starvation = document.getElementById("starvation");
    //获取换日恢复值
    var change = change_calc(stamina_value,happiness_value,health_value,starvation_value);
    var stamina_change = change["stamina_change"];
    var happiness_change = change["happiness_change"];
    var health_change = change["health_change"];
    var starvation_change = change["starvation_change"];
    //保留一位小数
    stamina_change = stamina_change.toFixed(1);
    happiness_change = happiness_change.toFixed(1);
    health_change = health_change.toFixed(1);
    starvation_change = starvation_change.toFixed(1);
    //修改数据
    if (stamina_change >= 0)
    {
        stamina.innerHTML = "精力 "+stamina_value+" / 100"+" + "+stamina_change;
    }
    else 
    {
        stamina.innerHTML = "精力 "+stamina_value+" / 100"+" - "+Math.abs(stamina_change);
    }
    if (happiness_change >= 0)
    {
        happiness.innerHTML = "快乐 "+happiness_value+" / 100"+" + "+happiness_change;
    }
    else 
    {
        happiness.innerHTML = "快乐 "+happiness_value+" / 100"+" - "+Math.abs(happiness_change);
    }
    if (health_change >= 0)
    {
        health.innerHTML = "健康 "+health_value+" / 100"+" + "+health_change;
    }
    else 
    {
        health.innerHTML = "健康 "+health_value+" / 100"+" - "+Math.abs(health_change);
    }
    if (starvation_change >= 0)
    {
        starvation.innerHTML = "饥饿 "+starvation_value+" / 100"+" - "+starvation_change;
    }
    else 
    {
        starvation.innerHTML = "饥饿 "+starvation_value+" / 100"+" + "+Math.abs(starvation_change);
    }
    //修改颜色
    //精力
    if (stamina_value <= 25)
    {
        stamina.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-danger")
    }
    else if (stamina_value <= 50)
    {
        stamina.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-warning")
    }
    else if (stamina_value <= 75)
    {
        stamina.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-success")
    }
    else
    {
        stamina.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated")
    }
    //快乐
    if (happiness_value <= 25)
    {
        happiness.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-danger")
    }
    else if (happiness_value <= 50)
    {
        happiness.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-warning")
    }
    else if (happiness_value <= 75)
    {
        happiness.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-success")
    }
    else
    {
        happiness.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated")
    }
    //健康
    if (health_value <= 25)
    {
        health.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-danger")
    }
    else if (health_value <= 50)
    {
        health.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-warning")
    }
    else if (health_value <= 75)
    {
        health.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-success")
    }
    else
    {
        health.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated")
    }
    //饥饿
    if (starvation_value <= 25)
    {
        starvation.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-danger")
    }
    else if (starvation_value <= 50)
    {
        starvation.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-warning")
    }
    else if (starvation_value <= 75)
    {
        starvation.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated bg-success")
    }
    else
    {
        starvation.setAttribute("class","progress-bar progress-bar-striped progress-bar-animated")
    }
    //设置值
    stamina.style.width = stamina_value + "%";
    happiness.style.width = happiness_value + "%";
    health.style.width = health_value + "%";
    starvation.style.width = starvation_value + "%";
}

//检查属性合法性
function check(stamina_value,happiness_value,health_value,starvation_value)
{
    //不能大于100
    if (stamina_value > 100)
    {
        stamina_value = 100;
    }
    if (happiness_value > 100)
    {
        happiness_value = 100;
    }
    if (health_value > 100)
    {
        health_value = 100;
    }
    if (starvation_value > 100)
    {
        starvation_value = 100;
    }
    //不能小于0
    if (stamina_value < 0)
    {
        stamina_value = 0;
    }
    if (happiness_value < 0)
    {
        happiness_value = 0;
    }
    if (health_value < 0)
    {
        health_value = 0;
    }
    if (starvation_value < 0)
    {
        starvation_value = 0;
    }
    //保留一位小数
    stamina_value = stamina_value.toFixed(1);
    happiness_value = happiness_value.toFixed(1);
    health_value = health_value.toFixed(1);
    starvation_value = starvation_value.toFixed(1);
    //转型
    stamina_value = Number(stamina_value);
    happiness_value = Number(happiness_value);
    health_value = Number(health_value);
    starvation_value = Number(starvation_value);
    //以json形式返回
    var value={"stamina_value":stamina_value,"happiness_value":happiness_value,"health_value":health_value,"starvation_value":starvation_value};
    return value;
}

//换日属性变更计算
function change_calc(stamina_value,happiness_value,health_value,starvation_value)
{
    //默认值24/1/1/0
    var stamina_change = 24;
    var happiness_change = 1;
    var health_change = 1;
    var starvation_change = 0;
    //饥饿改变10%
    starvation_change = starvation_value * 0.1
    //Q1宅院
    happiness_change += 0.2
    health_change += 0.2
    //计算精力
    //如果精力 < 25 则 *（精力 + 75）/ 100
    if (stamina_value < 25)
    {
        stamina_change *= (stamina_value + 75) / 100;
    }
    //如果快乐 > 75 则 *（快乐 + 25）/ 100
    if (starvation_value > 75)
    {
        stamina_change *= (happiness_value + 25) / 100;
    }
    //如果健康 < 75 则 *（健康 + 25） / 100
    if (health_value < 75)
    {
        stamina_change *= (health_value + 25) / 100;
    }
    //如果饥饿 < 75 则 *（饥饿 + 25）/ 100
    if (starvation_value < 75)
    {
        stamina_change *= (starvation_value + 25) / 100;
    }
    //计算快乐
    //快乐回复+6，低于40每低1点额外加成1/8
	happiness_change += Math.max(6, (88 - happiness_value) / 8);
	//如果精力 < 25 则 *（精力 + 25）/ 50 如果精力 > 75 则 *（精力 - 25）/ 50
    if (stamina_value < 25)
    {
        happiness_change *= (stamina_value + 25) / 50;
    }
    else if (stamina_value > 75)
    {
        happiness_change *= (stamina_value - 25) / 50;
    }
    //如果健康 > 75 则 *（健康 + 25）/ 100
    if (health_value > 75)
    {
        happiness_change *= (health_value + 25) / 100;
    }
    //如果饥饿 < 75 则 *（饥饿 + 25）/100
    if (starvation_value < 75)
    {
        happiness_change *= (starvation_value + 25) / 100;
    }
    //计算健康
    //健康回复+6，低于40每低1点额外加成1/8
        health_change += Math.max(6, (88 - health_value) / 8);
    //如果精力 < 25 则 -（25-精力）*0.2
    if (stamina_value < 25)
    {
        health_change -= (25 - stamina_value) * 0.2
    }
    //如果饥饿 < 75 则 -（75 - 饥饿）* 0.15
    if (starvation_value < 75)
    {
        health_change -= (75 - starvation_value) * 0.15;
    }
    //如果饥饿 < 75 则 *（饥饿 + 25）/100
    if (starvation_value < 75)
    {
        health_change *= (starvation_value + 25) / 100;
    }
	//如果精力 < 25 则 *（精力 + 25）/ 50 如果精力 > 75 则 *（精力 - 25）/ 50
	if (stamina_value < 25)
    {
        health_change *= (stamina_value + 25) / 50;
    }
    else if (stamina_value > 75)
    {
        health_change *= (stamina_value - 25) / 50;
    }
    //如果快乐 > 75 则 *（快乐 + 25）/ 100
    if (happiness_value > 75)
    {
        health_change *= (happiness_value + 25) / 100;
    }
    //转型
    stamina_change = Number(stamina_change);
    happiness_change = Number(happiness_change);
    health_change = Number(health_change);
    starvation_change = Number(starvation_change);
    //以json形式返回
    var change={"stamina_change":stamina_change,"happiness_change":happiness_change,"health_change":health_change,"starvation_change":starvation_change};
    return change;
}