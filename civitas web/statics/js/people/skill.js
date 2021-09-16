/*
技能Vue组件

组件1
名称:skill-show
用途:整体大框架
props:{
    prop:{
        uid:对应用户的uid
        username:对应用户的用户名
    },
    type:类型，index/people
}
data:{
    skills:参考接口文档getskills的data项
}

组件2
名称:skill-detail
用途:显示某个大类技能
props:{
    skill:参考接口文档getskills的data项中其中一项
}
data:{
    close_show:折叠/展开的显示
    skill_dict:门槛对应表
}
*/

Vue.component("skill-show", {
    props: ["prop","type"],
    data: function () {
        return {
            skills: [{}]
        }
    },
    created: function () {
        this.get_skill();
    },
    methods: {
        get_skill: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getskill/",
                withCredentials: true,
                params: {
                    uid: this.prop.uid,
                },
            })
            .then(function (response) {
                vm.skills = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template:`
    <div>
        <p class="main-char" v-if="type == 'index'">我的技能</p>
        <p class="main-char" v-else-if="type == 'people'">{{ prop.username }}的技能</p>
        <p class="explain">点击左侧“+”号，可以查看技能对应的经验。</p>
        <div class="skill-name" v-if="skills.length == 0 && type == 'index'">
            <p class="explain">您还没有技能，去工作或是演讲，副业以获得技能。</p>
        </div>
        <div class="skill-name" v-else-if="skills.length == 0 && type == 'people'">
            <p class="explain">{{ prop.username }}还没有技能</p>
        </div>
        <skill-detail v-for="(skill, index) in skills" v-bind:key="'skill'+index" v-bind:skill="skill"></skill-detail>
    </div>
    `
})

Vue.component("skill-detail", {
    props: ["skill"],
    data: function () {
        return {
            close_show: "+",
            close_status: false,
            skill_dict: {1:"学徒",2:"匠人",3:"匠师",4:"专家",5:"大师",6:"宗师",7:"大宗师"}
        }
    },
    created: function () {
        var vm = this;
        $("#skill-mini" + this.skill.id).on('shown.bs.collapse', function () {
            if (vm.close_show == "+") {
                vm.close_show = "-";
            }
            else if (vm.close_show == "-") {
                vm.close_show = "+";
            }
        })
        $("#skill-mini" + this.skill.id).on('hidden.bs.collapse', function () {
            if (vm.close_show == "+") {
                vm.close_show = "-";
            }
            else if (vm.close_show == "-") {
                vm.close_show = "+";
            }
        })
    },
    methods: {
        show_skill_mini: function () {
            if (this.close_show == "+") {
                this.close_show = "-";
            }
            else if (this.close_show == "-") {
                this.close_show = "+";
            }
            $("#skill-mini" + this.skill.id).collapse('toggle');
        }
    },
    template:`
    <div class="skill-box">
        <div class="skill-picture">
            <img v-bind:src="'civitas/icon/skill/'+skill.id+'/s.png'" width="60px" height="60px"/>
        </div>
        <div class="skill-right">
            <div class="skill-name">
                <p class="skill-name-left">{{ skill.name }}</p>
                <button class="close close_border" v-on:click="show_skill_mini()" v-bind:id="skill.id">{{ close_show }}</button>
                <p v-bind:class="'skill-name-right skill-name-right'+skill.level">{{ skill_dict[skill.level] }} {{ skill.skill.toFixed(2) }}</p>
            </div>
            <div class="collapse" v-bind:id="'skill-mini'+skill.id">
                <div class="skill-mini" v-for="skill_mini in skill.list" v-bind:key="'skill_mini'+skill_mini.id">
                    <img v-bind:src="'civitas/icon/skill/'+skill.id+'/'+skill_mini.id+'.png'" width="30px" height="30px"/>
                    <p>{{ skill_mini.name }} {{ (skill_mini.skill * 100).toFixed(1) }}%</p>
                </div>
            </div>
        </div>
    </div>
    `
})