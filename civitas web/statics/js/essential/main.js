/*
加载主vm
*/

var main_vm;

function load_main_vm(status,uid) {
    //随机事件组件
    Vue.component("ranevent-modal", {
        props: ["prop"],
        methods: {
            hide_modal: function (){
                this.$emit("hide_modal");
            },
            next_modal: function (url){
                this.$emit("hide_modal");
                this.$emit("next_modal",url);
            }
        },
        template:`
        <div class="modal fade" id="ranevent" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content modal-background">
                    <div class="modal-body bottomline-dashed">
                      <p class="modal-title-text">{{ prop.title }}</p>
                      <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    </div>
                    <div class="modal-body bottomline-dashed">
                        <p>{{ prop.statement }}</p>
                    </div>
                    <div class="modal-body ranevent-option" v-if="prop.type == 'work_strategy'">
                        <button 
                            type="button" 
                            class="btn" 
                            v-on:click="hide_modal" 
                            v-for="index in [...Array(prop.option_text.length).keys()]">
                            <img v-bind:src="'civitas/icon/work/Strategy_'+index+'.png'"/>
                            {{ prop.option_text[index] }}
                        </button>
                    </div>
                    <div class="modal-body ranevent-option" v-else>
                        <button 
                            type="button" 
                            class="btn" 
                            v-on:click="hide_modal" 
                            v-for="index in [...Array(prop.option_text.length).keys()]">
                            <img v-bind:src="'civitas/icon/choices/Choice_'+index+'.png'"/>
                            {{ prop.option_text[index] }}
                        </button>
                    </div>
                </div>
            </div>
        </div>`
    })
    //上导航栏组件
    Vue.component("top-navigator", {
        props: ["prop"],
        data: function () {
            return {
                total_day: 0,
                season: "春天",
                year: 0,
                hour: 0,
                minute: 0,
                height: 0
            }
        },
        created: function () {
            this.get_date();
            window.addEventListener("resize", this.get_height);
        },
        mounted: function () {
            this.get_height();
        },
        methods: {
            get_height: function () {
                this.height = this.$el.offsetHeight;
                this.$emit("height_change", this.height)
            },
            get_date: function () {
                var vm = this;
                axios({
                    method: "get",
                    url: "https://api.trickydeath.xyz/getdate/",
                    withCredentials: true
                })
                .then(function (response) {
                    var json_str_data = response.data.data;
                    vm.total_day = json_str_data.total_day;
                    vm.season = json_str_data.season;
                    var time = json_str_data.time;
                    vm.year = json_str_data.year;
                    var reg = /\d{2}/g;
                    var time2 = time.match(reg);
                    vm.hour = time2[0];
                    vm.minute = time2[1];
                })
                .catch(function (error) {
                    console.log(error);
                })
            },
            log_out: function () {
                axios({
                    method: "get",
                    url: "https://api.trickydeath.xyz/logout/",
                    withCredentials: true
                })
                .then(function (response) {
                    var json_str_data = response.data.data;
                    if (json_str_data.status == 1) {
                        window.location.assign("login.html");
                    }
                })
                .catch(function (error) {
                    console.log(error);
                })
            }
        },
        template: `
        <nav class="navigator" role="navigation">
            <img src="civitas/img/CIVITAS2.png" width="120px" height="25px" class="civitas2"/>
            <p class="vertime">Pre-Alpha 0.0.10<br>Y{{ year }} {{ season }} D{{ total_day }} {{ hour }}:{{ minute }}</p>
            <a v-if="prop.status == 1" href="#street"><img src="civitas/svg/common/street.svg" width="22px" height="22px"/>城市</a>
            <a v-if="prop.status == 1" href="map.html"><img src="civitas/svg/common/map.svg" width="22px" height="22px"/>地图</a>
            <a v-if="prop.status == 1" href="#market"><img src="civitas/svg/common/market.svg" width="22px" height="22px"/>市场</a>
            <a href="error.html"><img src="civitas/svg/common/blog.svg" width="22px" height="22px"/>开发日志</a>
            <span class="signup-in">
                <img v-if="prop.status == 1" v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+prop.uid" width="40px" height="40px"/>
                <a v-if="prop.status == 1" href="javascript:void(0)" v-on:click="log_out">注销</a>
                <a v-if="prop.status == 0" href="login.html">登录</a>
                <a v-if="prop.status == 0" href="register.html">注册</a>
            </span>
        </nav>
        `
    })
    //侧导航栏组件
    Vue.component("left-navigator", {
        props: ["prop"],
        data: function () {
            return {
            }
        },
        template: `
        <div class="left-navigator">
            <div class="bottomline avatar">
                <a v-bind:href="'people.html?uid='+prop.uid">
                    <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+prop.uid" class="img-thumbnail" width="80px" height="80px"/>
                </a>
                <div class="level">
                    <a v-bind:href="'people.html?uid='+prop.uid">{{ prop.username }}</a>
                    <p>等级 100级</p>
                    <div class="progress">
                        <div class="progress-bar bg-warning progress-bar-striped progress-bar-animated" style="width: 50%">
                            <p>经验 1000 / 2000</p>
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
                    <a href="sideline.html?type=education">我的教育</a>
                </div>
                <div class="bottomline">
                    <p class="menu">我的交际圈</p>
                    <a href="#home">我的人际关系</a>
                    <a v-bind:href="'social.html?uid='+prop.uid">我的社交活动</a>
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
    main_vm = new Vue({
        el: "#main",
        data: {
            navigator_width: 0,
            b: [1,5,6,7,8,9,10,11,12,15,17,18,80,20,21,22],
            uid: uid,
            someone_uid: undefined,
            someone_detail: {},
            speech_input: "",
            ranevent_prop: {
                title:"",
                statement:"",
                type:"normal",
                option_text:[]
            },
            weather_prop: {
                total_day:0,
                time:0,
                year:0,
                season:"春天",
                day: 0
            },
            user_prop: {
                uid: uid,
                status: {stamina: 0, happiness: 0, health: 0, starvation: 0}, 
                status_change: {stamina_change: 0, happiness_change: 0, health_change: 0, starvation_change: 0}
            },
            top_navigator_prop: {
                uid: uid,
                status: status
            }
        },
        created: function () {
            var vm = this;
            //获取自己的信息
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getuserdetail/",
                withCredentials: true,
                params: {
                    uid: this.uid,
                },
            })
            .then(function (response) {
                //在user_prop中添加username属性
                vm.$set(vm.user_prop,"username",response.data.data.username);
            })
            .catch(function (error) {
                console.log(error);
            })
            //临时填充城市信息
            this.$set(this.user_prop,"city","长安");
            this.$set(this.user_prop,"cityid",1);
            //如果有uid参数的话，拿到uid对应用户信息
            try {
                this.someone_uid = get_parameter_value("uid");
            }
            catch (error) {}
            if (this.someone_uid != undefined) {
                axios({
                    method: "get",
                    url: "https://api.trickydeath.xyz/getuserdetail/",
                    withCredentials: true,
                    params: {
                        uid: this.someone_uid,
                    },
                })
                .then(function (response) {
                    //在someone_detail中添加username属性
                    vm.$set(vm.someone_detail,"username",response.data.data.username);
                })
                .catch(function (error) {
                    console.log(error);
                })
                this.$set(this.someone_detail,"uid",this.someone_uid);
                //临时填充城市信息
                this.$set(this.someone_detail,"city","长安");
                this.$set(this.someone_detail,"cityid",1);
            }
            //获取日期信息
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getdate/",
                withCredentials: true,
            })
            .then(function (response) {
                vm.weather_prop = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            })
            //获取用户状态
            this.get_status();
        },
        methods: {
            height_change: function (height) {
                this.navigator_width = height;
            },
            //随机事件相关
            show_ranevent_modal: function () {
                $("#ranevent").modal("show");
            },
            hide_ranevent_modal: function () {
                $("#ranevent").modal("hide");
            },
            get_ranevent: function (url) {
                var vm = this;
                axios({
                    method: "get",
                    url: url,
                    withCredentials: true,
                })
                .then(function (response) {
                    var json_str_data = response.data.data;
                    vm.ranevent_prop = json_str_data.ranevent_data;
                })
                .catch(function (error) {
                    console.log(error);
                });
            },
            get_ranevent_by_data: function (data) {
                console.log(data);
                this.ranevent_prop = data;
                this.show_ranevent_modal();
            },
            //刷新演讲
            speech_refresh: function () {
                this.$refs.speech_popular.get_speech_popular();
                this.$refs.speech_main.page_turn(1);
            },
            //获取用户状态
            get_status: function () {
                var vm = this;
                axios({
                    method: "get",
                    url: "https://api.trickydeath.xyz/getstatus/",
                    withCredentials: true,
                })
                .then(function (response) {
                    var json_str_data = response.data.data;
                    status_today = json_str_data.today;
                    status_change = json_str_data.tomorrow;
                    if (status_change.stamina_change >= 0) {
                        status_change.stamina_change = " + " + status_change.stamina_change.toFixed(1);
                    }
                    else {
                        status_change.stamina_change = " - " + Math.abs(status_change.stamina_change).toFixed(1);
                    }
                    if (status_change.happiness_change >= 0) {
                        status_change.happiness_change = " + " + status_change.happiness_change.toFixed(1);
                    }
                    else {
                        status_change.happiness_change = " - " + Math.abs(status_change.happiness_change).toFixed(1);
                    }
                    if (status_change.health_change >= 0) {
                        status_change.health_change = " + " + status_change.health_change.toFixed(1);
                    }
                    else {
                        status_change.health_change = " - " + Math.abs(status_change.health_change).toFixed(1);
                    }
                    if (status_change.starvation_change >= 0) {
                        status_change.starvation_change = " + " + status_change.starvation_change.toFixed(1);
                    }
                    else {
                        status_change.starvation_change = " - " + Math.abs(status_change.starvation_change).toFixed(1);
                    }
                    vm.$set(vm.user_prop,"status",status_today);
                    vm.$set(vm.user_prop,"status_change",status_change);
                })
                .catch(function (error) {
                    console.log(error);
                })
            }
        }
    })
}