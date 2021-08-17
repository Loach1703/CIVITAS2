/*
副业与教育
do_sideline：进行副业
*/
var sideline_vm;

function do_sideline(sideline_id,type_id=1)
{
    /*参数说明：
    sideline_id：副业编号
    type_id：类型，如果是副业则为1（默认）
    */
    if (isNaN(sideline_id) || isNaN(type_id))
    {
        return;
    }
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function()
    {
        var str = xmlhttp.responseText;
        var json_str = JSON.parse(str);
        if (json_str["status"] == 1)
        {
            status_update();
            sideline_vm.updata_skill();
        }
    }
    xmlhttp.open("POST","https://api.trickydeath.xyz/dosideline/",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.withCredentials = true;
    xmlhttp.send("sidelineid="+sideline_id+"&typeid="+type_id);
}

function load_education()
{
    Vue.component("education-display", {
        props: ["education"],
        template: `
            <div class="sideline-box bottomline-dashed">
                <img v-bind:src="'civitas/icon/skill/'+education.id+'/s.png'" width="70px" height="70px" class="sideline-mainimg"/>
                <span class="sideline-text1">
                    <p class="sideline-education-name">{{ education.name }}</p>
                    <p v-bind:class="'skill-name-right'+education.level" class="skill-name-education">{{ education.level_name }} {{ education.skill.toFixed(2) }}</p>
                    <div class="progress status">
                        <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" v-bind:style="'width:'+(education.comprehension*100).toFixed(1)+'%'">悟性 {{ (education.comprehension*100).toFixed(1) }}% / 100%</div>
                    </div>
                </span>
                <span class="sideline-text2">
                    <p class="sideline-education-chance">突破概率 {{ (education.eureka_probability*100).toFixed(1) }}%</p>
                </span>
                <button class="btn btn-primary" v-bind:onclick="'do_sideline('+education.id+',2)'">教育</button>
            </div>
        `
    });
    sideline_vm = new Vue({
        el: "#main",
        data: {
            skills: []
        },
        created: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getskill/",
                withCredentials: true
            })
            .then(function (response) {
                var json_str_data = response.data.data;
                var skill_dict = {1:"学徒",2:"匠人",3:"匠师",4:"专家",5:"大师",6:"宗师",7:"大宗师"};
                for (i=0; i<json_str_data.length; i++) 
                {
                    json_str_data[i].level_name = skill_dict[json_str_data[i].level];
                    vm.skills.push(json_str_data[i]);
                }
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        computed: {
        },
        methods: {
            test: function(){
                this.skills.push({"id": 2, "name": "\u91c7\u4f10", "skill": 4.4637511876676115, "level": 1, "level_name": "学徒", "comprehension": 0.44637511876676115, "eureka_probability": 0.48187559383380574, "list": [{"id": 1, "name": "\u91c7\u96c6", "skill": 0.28837458781690084}]});
            },
            updata_skill: function () {
                var vm = this;
                axios({
                    method: "get",
                    url: "https://api.trickydeath.xyz/getskill/",
                    withCredentials: true
                })
                .then(function (response) {
                    var json_str_data = response.data.data;
                    var skill_dict = {1:"学徒",2:"匠人",3:"匠师",4:"专家",5:"大师",6:"宗师",7:"大宗师"};
                    for (i=0; i<json_str_data.length; i++) 
                    {
                        json_str_data[i].level_name = skill_dict[json_str_data[i].level];
                        vm.skills[i] = json_str_data[i]
                    }
                })
                .catch(function (error) {
                    console.log(error);
                })
            }
        }
    })
}