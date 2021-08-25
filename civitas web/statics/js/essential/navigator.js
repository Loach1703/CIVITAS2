/*
导航栏
navigator：根据是否登录，写入不同的导航栏
date_navigator：获取日期，显示在导航栏上
left_navigator：显示左侧导航栏
*/

function navigator(status,uid)
{
    /*参数说明：
    status：登录状态，由is_login函数返回值得到
    uid：用户id
    */
    if (uid == null)
    {
        uid = 0;
    }
    var nav = document.getElementById("navigator");
    //已登录
    if (status == 1)
    {
        nav.innerHTML = `
            <img src="civitas/img/CIVITAS2.png" width="120px" height="25px" class="civitas2"/>
            <span class="vertime">Pre-Alpha 0.0.9
                <p id="time" class="time"></p>
            </span>
            <span>
                <a href="#street"><img src="civitas/svg/common/street.svg" width="22px" height="22px"/>县城</a>
                <a href="map.html"><img src="civitas/svg/common/map.svg" width="22px" height="22px"/>地图</a>
            </span>
            <span class="market-main" id="market">
                <a href="#market"><img src="civitas/svg/common/market.svg" width="22px" height="22px"/>市场</a>
                <div id="market-down" class="market-dropdown hide">
                    <a href="#square"><img src="civitas/svg/common/goods.svg" width="22px" height="22px"/>物资市场</a>
                    <a href="#square"><img src="civitas/svg/common/recruit.svg" width="22px" height="22px">招聘市场</a>
                    <a href="#square"><img src="civitas/svg/common/estate.svg" width="22px" height="22px"/>不动产市场</a>
                </div>
            </span>
            <span>
                <a href="blog/1.html"><img src="civitas/svg/common/blog.svg" width="22px" height="22px"/>开发日志</a>
            </span>
            <span class="signup-in">
                <img src="https://api.trickydeath.xyz/getavatar/?uid=`+uid+`" width="40px" height="40px"/>
                <a href="javascript:void(0)" onclick="log_out()">注销</a>
            </span>`
    }
    else
    {
        nav.innerHTML = `
            <img src="civitas/img/CIVITAS2.png" width="120px" height="25px" class="civitas2"/>
            <span class="vertime">Pre-Alpha 0.0.9
                <p id="time" class="time"></p>
            </span>
            <span>
                <a href="blog/1.html"><img src="civitas/svg/common/blog.svg" width="22px" height="22px"/>开发日志</a>
            </span>
            <span class="signup-in">
                <a href="login.html">登录</a>
                <a href="register.html">注册</a>
            </span>`
    }
    date_navigator();
}

function date_navigator()
{
    var xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange= function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var str = xmlhttp.responseText;
            var json_str = JSON.parse(str);
            var total_day = json_str["data"]["total_day"];
            var season = json_str["data"]["season"];
            var time = json_str["data"]["time"];
            var reg = /\d{2}/g;
            var time2 = time.match(reg);
            var hour = time2[0];
            var minute = time2[1];
            document.getElementById("time").innerHTML = season+" D"+total_day+" "+hour+":"+minute;
		}
	}
    xmlhttp.open("GET","https://api.trickydeath.xyz/getdate/",true);
    xmlhttp.send();
}

var leftnav_vm;

function left_navigator(uid)
{
    Vue.component("left-navigator", {
        props: ["prop"],
        data: function () {
            return {
            }
        },
        template: `
        <div class="left-navigator">
            <div class="bottomline">
                <a v-bind:href="'people.html?uid='+prop.uid" class="avatar">
                    <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+prop.uid" class="img-thumbnail" width="80px" height="80px"/>
                </a>
                <div class="level">
                    <a v-bind:href="'people.html?uid='+prop.uid" id="username">{{ prop.username }}</a>
                    <p>等级 100级</p>
                    <div class="progress levelbar">
                        <div class="progress-bar bg-warning progress-bar-striped progress-bar-animated" style="width: 50%">
                            <p class="xp">经验 1000 / 2000</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bottomline">
                <p class="menu">我的状态</p>
                <div id="status">
                    <div class="progress status">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" 
                            v-bind:class="{ 'bg-danger': prop.status.stamina < 20,'bg-warning': prop.status.stamina < 40 && prop.status.stamina >= 20,'bg-success': prop.status.stamina < 60 && prop.status.stamina >= 40,'bg-info': prop.status.stamina < 80 && prop.status.stamina >= 60 }" 
                            v-bind:style="'width:'+prop.status.stamina+'%'">精力 {{ prop.status.stamina }} / 100 {{ prop.status_change.stamina_change }}
                        </div>
                    </div>
                    <div class="progress status">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" 
                            v-bind:class="{ 'bg-danger': prop.status.happiness < 20,'bg-warning': prop.status.happiness < 40 && prop.status.happiness >= 20,'bg-success': prop.status.happiness < 60 && prop.status.happiness >= 40,'bg-info': prop.status.happiness < 80 && prop.status.happiness >= 60 }" 
                            v-bind:style="'width:'+prop.status.happiness+'%'">快乐 {{ prop.status.happiness }} / 100 {{ prop.status_change.happiness_change }}
                        </div>
                    </div>
                    <div class="progress status">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" 
                            v-bind:class="{ 'bg-danger': prop.status.health < 20,'bg-warning': prop.status.health < 40 && prop.status.health >= 20,'bg-success': prop.status.health < 60 && prop.status.health >= 40,'bg-info': prop.status.health < 80 && prop.status.health >= 60 }" 
                            v-bind:style="'width:'+prop.status.health+'%'">健康 {{ prop.status.health }} / 100 {{ prop.status_change.health_change }}
                        </div>
                    </div>
                    <div class="progress status">
                        <div class="progress-bar progress-bar-striped progress-bar-animated" 
                            v-bind:class="{ 'bg-danger': prop.status.starvation < 20,'bg-warning': prop.status.starvation < 40 && prop.status.starvation >= 20,'bg-success': prop.status.starvation < 60 && prop.status.starvation >= 40,'bg-info': prop.status.starvation < 80 && prop.status.starvation >= 60 }" 
                            v-bind:style="'width:'+prop.status.starvation+'%'">饥饿 {{ prop.status.starvation }} / 100 {{ prop.status_change.starvation_change }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="left-navigator-option">
                <div class="bottomline">
                    <p class="menu">我的CIVITAS</p>
                    <a href="index.html">我的CIVITAS</a>
                    <a href="#news">我的通知</a>
                    <a href="settings.html">我的设置</a>
                </div>
                <div class="bottomline">
                    <p class="menu">我的生活</p>
                    <a href="create_recipe.html">我的食谱</a>
                    <a href="#home">我的藏书</a>
                    <a href="sideline.html">我的副业</a>
                    <a href="education.html">我的教育</a>
                </div>
                <div class="bottomline">
                    <p class="menu">我的交际圈</p>
                    <a href="#home">我的人际关系</a>
                    <a href="#news">我的社交活动</a>
                </div>
                <div class="bottomline">
                    <p class="menu">我的资产</p>
                    <a v-bind:href="'depository.html?uid='+prop.uid">我的库房</a>
                    <a href="#news">我的私人交易</a>
                    <a href="#news">我管理的不动产</a>
                    <a href="#home">我拥有的不动产</a>
                </div>
            </div>
        </div>
        `
    })
    leftnav_vm = new Vue({
        el: "#left-navigator",
        data: {
            uid: uid,
            username: "username",
            status: {},
            status_change: {},
            prop: {
                uid: uid,
                username: this.username,
                status: {stamina: 0, happiness: 0, health: 0, starvation: 0}, 
                status_change: {stamina_change: 0, happiness_change: 0, health_change: 0, starvation_change: 0}
            }
        },
        created: function () {
            var vm = this;
            this.get_status();
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getuserdetail/",
                withCredentials: true,
                params: {
                    uid: this.uid
                },
            })
            .then(function (response) {
                var json_str_data = response.data.data;
                vm.username = json_str_data.username;
                vm.prop.uid = vm.uid;
                vm.prop.username = vm.username;
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        methods: {
            get_status: function () {
                var vm = this;
                axios({
                    method: "get",
                    url: "https://api.trickydeath.xyz/getstatus/",
                    withCredentials: true,
                })
                .then(function (response) {
                    var json_str_data = response.data.data;
                    vm.status = json_str_data.today;
                    vm.status_change = json_str_data.tomorrow;
                    if (vm.status_change.stamina_change >= 0) {
                        vm.status_change.stamina_change = " + " + vm.status_change.stamina_change.toFixed(1);
                    }
                    else {
                        vm.status_change.stamina_change = " - " + Math.abs(vm.status_change.stamina_change).toFixed(1);
                    }
                    if (vm.status_change.happiness_change >= 0) {
                        vm.status_change.happiness_change = " + " + vm.status_change.happiness_change.toFixed(1);
                    }
                    else {
                        vm.status_change.happiness_change = " - " + Math.abs(vm.status_change.happiness_change).toFixed(1);
                    }
                    if (vm.status_change.health_change >= 0) {
                        vm.status_change.health_change = " + " + vm.status_change.health_change.toFixed(1);
                    }
                    else {
                        vm.status_change.health_change = " - " + Math.abs(vm.status_change.health_change).toFixed(1);
                    }
                    if (vm.status_change.starvation_change >= 0) {
                        vm.status_change.starvation_change = " + " + vm.status_change.starvation_change.toFixed(1);
                    }
                    else {
                        vm.status_change.starvation_change = " - " + Math.abs(vm.status_change.starvation_change).toFixed(1);
                    }
                    vm.prop.status = vm.status;
                    vm.prop.status_change = vm.status_change;
                })
                .catch(function (error) {
                    console.log(error);
                })
            }
        }
    })
}