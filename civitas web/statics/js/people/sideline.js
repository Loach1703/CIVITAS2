/*
副业，教育Vue组件

组件1
名称:sideline-display
用途:显示副业，教育
data:{
    type:类型，默认为副业
}
*/

Vue.component("sideline-display", {
    data: function () {
        return {
            type: "sideline",
            datas: [],
            skill_level_dict: {1:"学徒",2:"匠人",3:"匠师",4:"专家",5:"大师",6:"宗师",7:"大宗师"},
            skill_dict: {
                1:["耕作","粮食种植","蔬果种植","经济作物种植","开垦"],
                2:["采伐","采集","伐木","勘探","开采"],
                3:["建设","建筑","维护"],
                4:["加工","冶炼","金属锻造","纺织","食品加工","木石加工"],
                5:["社交","雄辩","交际","文书","管理"],
                6:["舟车","陆上运输","水上运输","捕捞"],
                7:["畜牧","狩猎","家禽养殖","家畜养殖"]
            }
        }
    },
    created: function () {
        if (get_parameter_value("type") == "education")
        {
            this.type = "education";
        }
        if (this.type == "education")
        {
            document.title = "我的教育 - 古典社会模拟 CIVITAS2";
            this.get_skill();
        }
        else if (this.type == "sideline")
        {
            document.title = "我的副业 - 古典社会模拟 CIVITAS2";
            this.datas = [
                {id:1,name:"采集",skill_id:"2",skill_mini_id:"1",statement:"进行这种副业不需要原料。",start_statement:"出发采集"},
                {id:2,name:"狩猎",skill_id:"7",skill_mini_id:"1",statement:"进行这种副业不需要原料。",start_statement:"出发狩猎"}
            ]
        }
    },
    methods: {
        get_skill: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getskill/",
                withCredentials: true
            })
            .then(function (response) {
                vm.datas = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        do_sideline: function (id) {
            var vm = this;
            var post_data = new URLSearchParams();
            post_data.append("sidelineid",id);
            if (this.type == "education")
            {
                post_data.append("typeid",2);
            }
            else if (this.type == "sideline")
            {
                post_data.append("typeid",1);
            }
            axios({
                method: "post",
                url: "https://api.trickydeath.xyz/dosideline/",
                withCredentials: true,
                data: post_data
            })
            .then(function (response) {
                var json_str_data = response.data.data;
                console.log(json_str_data);
                if (vm.type == "education")
                {
                    console.log("education");
                    vm.get_skill();
                }
                else if (vm.type == "sideline")
                {
                    if (json_str_data.material == "一无所获") {
                        vm.$emit("showre",
                            {title:json_str_data.sideline_name+"失败",
                            statement:"在今天的"+json_str_data.sideline_name+"中，你一无所获。",
                            type:"normal",
                            option_text:["那就这样吧。"]
                        })
                    }
                    else {
                        vm.$emit("showre",
                            {title:json_str_data.sideline_name+"成功",
                            statement:"在今天的"+json_str_data.sideline_name+"中，你得到了"+json_str_data.count.toFixed(2)+"单位的"+json_str_data.material_name+"。",
                            type:"normal",
                            option_text:["那就这样吧。"]
                        })
                    }
                }
                vm.get_status();
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template: `
    <div class="main-double">
        <template v-if="type == 'education'">
            <p class="main-char">我的教育</p>
            <p class="author">进行教育能获得悟性并给你额外的突破机会，从而增加你突破门槛的概率，同时你也能获得技能。
                <br>一次副业/教育消耗15/3/3/4属性值，但要注意，你当日副业/教育的次数越多，消耗的属性值（除饥饿外）就会成倍增加。今天你副业/教育了<strong></strong>次。    
            </p>
            <div class="sideline-box bottomline-dashed" v-for="education in datas" v-bind:key="education.id">
                <img v-bind:src="'civitas/icon/skill/'+education.id+'/s.png'" width="70px" height="70px" class="sideline-mainimg"/>
                <span class="sideline-text1">
                    <p class="sideline-education-name">{{ education.name }}</p>
                    <p v-bind:class="'skill-name-right'+education.level" class="skill-name-education">{{ skill_level_dict[education.level] }} {{ education.skill.toFixed(2) }}</p>
                    <div class="progress status">
                        <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" v-bind:style="'width:'+(education.comprehension*100).toFixed(1)+'%'">悟性 {{ (education.comprehension*100).toFixed(1) }}% / 100%</div>
                    </div>
                </span>
                <span class="sideline-text2">
                    <p class="sideline-education-chance">突破概率 {{ (education.eureka_probability*100).toFixed(1) }}%</p>
                </span>
                <button class="btn btn-primary" v-on:click="do_sideline(education.id)">教育</button>
            </div>
        </template>
        <template v-else-if="type == 'sideline'">
            <p class="main-char">我的副业</p>
            <p class="author">副业能够获得物资，并锻炼你的技能，采集和狩猎能随机获得一些物资，而其他类型的副业则是加工型的。
                <br>一次副业/教育消耗15/3/3/4属性值，但要注意，你当日副业/教育的次数越多，消耗的属性值（除饥饿外）就会成倍增加。今天你副业/教育了<strong></strong>次。
            </p>
            <div class="sideline-box bottomline-dashed" v-for="sideline in datas" v-bind:key="sideline.id">
                <img v-bind:src="'civitas/icon/sideline/'+sideline.id+'.png'" width="70px" height="70px" class="sideline-mainimg"/>
                <span class="sideline-text1">
                    <p class="sideline-name">{{ sideline.name }}<br></p>
                    <p>技能</p>
                    <img v-bind:src="'civitas/icon/skill/'+sideline.skill_id+'/s.png'" width="20px" height="20px"/>
                    <p class="sideline-skill">{{ skill_dict[sideline.skill_id][0] }}</p>
                    <p>经验</p>
                    <img v-bind:src="'civitas/icon/skill/'+sideline.skill_id+'/'+sideline.skill_mini_id+'.png'" width="20px" height="20px"/>
                    <p class="sideline-skill-mini">{{ skill_dict[sideline.skill_id][sideline.skill_mini_id] }}</p>
                    <p class="sideline-need"><br>{{ sideline.statement }}</p>
                </span>
                <span class="sideline-text2">
                    <p>预期产能</p>
                    <p class="sideline-name"></p>
                </span>
                <button class="btn btn-primary" v-on:click="do_sideline(sideline.id)">{{ sideline.start_statement }}</button>
            </div>
        </template>
    </div>
    `
});