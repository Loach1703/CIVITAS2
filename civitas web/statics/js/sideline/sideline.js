/*
副业与教育
do_sideline：进行副业
*/

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
    }
    xmlhttp.open("POST","https://api.trickydeath.xyz/dosideline/",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.withCredentials = true;
    xmlhttp.send("sidelineid="+sideline_id+"&typeid="+type_id);
}

Vue.component("education-display", {
    data: function () {
        return {
            skills: [],
            skill_dict: {1:"学徒",2:"匠人",3:"匠师",4:"专家",5:"大师",6:"宗师",7:"大宗师"}
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
                withCredentials: true
            })
            .then(function (response) {
                vm.skills = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template: `
    <div>
        <p class="main-char">我的教育</p>
        <p class="author">进行教育能获得悟性并给你额外的突破机会，从而增加你突破门槛的概率，同时你也能获得技能。</p>
        <div class="sideline-box bottomline-dashed" v-for="education in skills" v-bind:key="education.id">
            <img v-bind:src="'civitas/icon/skill/'+education.id+'/s.png'" width="70px" height="70px" class="sideline-mainimg"/>
            <span class="sideline-text1">
                <p class="sideline-education-name">{{ education.name }}</p>
                <p v-bind:class="'skill-name-right'+education.level" class="skill-name-education">{{ skill_dict[education.level] }} {{ education.skill.toFixed(2) }}</p>
                <div class="progress status">
                    <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" v-bind:style="'width:'+(education.comprehension*100).toFixed(1)+'%'">悟性 {{ (education.comprehension*100).toFixed(1) }}% / 100%</div>
                </div>
            </span>
            <span class="sideline-text2">
                <p class="sideline-education-chance">突破概率 {{ (education.eureka_probability*100).toFixed(1) }}%</p>
            </span>
            <button class="btn btn-primary" v-bind:onclick="'do_sideline('+education.id+',2)'" v-on:click="get_skill">教育</button>
        </div>
    </div>
    `
});