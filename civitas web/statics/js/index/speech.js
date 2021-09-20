/*
演讲Vue组件

组件1
名称:speech-main
用途:显示演讲，翻页
props:{
    prop:{
        uid:对应用户的uid
        username:对应用户的用户名
    },
    type:类型，index/tag/people
}
data:{
    speechs:获取的所有演讲
    total_page:总页数
    page:当前页数
    page_swap:跳转到的页数
    tagid:标签id,
    tagname:标签名字,
}
methods:{
    get_speech_type:根据type决定ajax参数
    get_speech_index:主页使用
    get_speech_tag:演讲话题页使用
    get_speech_people:个人主页使用
    page_turn:翻页
    speech_attitude:发表演讲态度
}

组件2
名称:skill-popular
用途:显示热门演讲
data:{
    speech:热门演讲内容
}
methods:{
    get_speech_popular:获取热门演讲
    speech_attitude:发表演讲态度
}

组件3
名称:skill-deliver
用途:发表演讲
data:{
    speech_input:演讲内容
    speech_tips:提示信息
}
methods:{
    give_speech:发表演讲
}
*/

Vue.component("speech-main", {
    props: ["prop","type"],
    data: function () {
        return {
            speechs: [],
            total_page: 0,
            page: 1,
            page_swap: undefined,
            tagid: "",
            tagname: "",
        }
    },
    created: function () {
        this.get_speech_type();
    },
    methods: {
        get_speech_type: function() {
            if (this.type == "index") {
                this.get_speech_index();
            }
            else if (this.type == "tag") {
                this.tagid = get_parameter_value("tagid");
                this.get_speech_tag();
            }
            else if (this.type == "people") {
                this.get_speech_people();
            }
        },
        get_speech_index: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getspeech/",
                withCredentials: true,
                params: {
                    page: this.page
                },
            })
            .then(function (response) {
                var json_str_data = response.data.data;
                vm.speechs = json_str_data.datalist;
                vm.total_page = json_str_data.total_page;
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        get_speech_tag: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getspeech/",
                withCredentials: true,
                params: {
                    page: this.page,
                    tagid: this.tagid
                },
            })
            .then(function (response) {
                var json_str_data = response.data.data;
                vm.speechs = json_str_data.datalist;
                vm.total_page = json_str_data.total_page;
                vm.tagname = json_str_data.tagname;
                document.title = "#" + json_str_data.tagname + "# - 古典社会模拟 CIVITAS2";
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        get_speech_people: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getspeech/",
                withCredentials: true,
                params: {
                    page: this.page,
                    uid: this.prop.uid
                },
            })
            .then(function (response) {
                var json_str_data = response.data.data;
                vm.speechs = json_str_data.datalist;
                vm.total_page = json_str_data.total_page;
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        page_turn: function (new_page) {
            if (isNaN(new_page)) {
                return;
            }
            this.page = new_page;
            this.get_speech_type();
        },
        speech_attitude: function (attitude,textid) {
            var vm = this;
            var post_data = new URLSearchParams();
            post_data.append("attitude",attitude);
            post_data.append("textid",textid);
            axios({
                method: "post",
                url: "https://api.trickydeath.xyz/assess/",
                withCredentials: true,
                data: post_data
            })
            .then(function (response) {
                vm.$emit("refresh");
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template:`
    <div>
        <p class="main-char" v-if="type == 'index'">本地演讲</p>
        <p class="main-char" v-else-if="type == 'tag'">#{{ tagname }}#</p>
        <p class="main-char" v-else-if="type == 'people'">{{ prop.username }}的演讲</p>
        <p class="explain" v-if="type == 'index' && speechs.length == 0">这里还没有人发表过演讲。</p>
        <p class="explain" v-else-if="type == 'tag' && speechs.length == 0">#{{ tagname }}#还没有演讲。</p>
        <p class="explain" v-else-if="type == 'people' && speechs.length == 0">{{ prop.username }}还没有发表过演讲。</p>
        <div class="speech bottomline-dashed" v-for="speech in speechs">
            <span class="speech-avatar">
                <a v-bind:href="'people.html?uid='+speech.uid">
                    <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+speech.uid" class="img-thumbnail" width="50px" height="50px">
                </a>
                <span class="speech-content">
                    <a v-bind:href="'people.html?uid='+speech.uid">{{ speech.username }}</a>
                    <p v-html="'：'+speech.text"></p>
                </span>
            </span>
            <span class="speech-bottom">
                <p>本地演讲，第{{ speech.day }}天，{{ speech.time }}</p>
            </span>
            <span class="speech-bottom">
                <a href="javascript:void(0)" v-on:click="speech_attitude(1,speech.textid)" v-bind:class="{ 'speech-attitude' : speech.my_attitude == 1 }">欢呼({{ speech.cheer }}) </a>
                <a href="javascript:void(0)" v-on:click="speech_attitude(2,speech.textid)" v-bind:class="{ 'speech-attitude' : speech.my_attitude == 2 }">关注({{ speech.onlooker }}) </a>
                <a href="javascript:void(0)" v-on:click="speech_attitude(3,speech.textid)" v-bind:class="{ 'speech-attitude' : speech.my_attitude == 3 }">倒彩({{ speech.catcall }})</a>
            </span>
        </div>
        <div id="speech-page-paginator" class="speech-page-paginator"></div>
        <div class="speech-page-paginator">
            <template v-if="total_page <= 7">
                <template v-for="among_page in [...Array(total_page).keys()]">
                    <span class="thispage" v-if="page == among_page + 1">{{ among_page + 1 }}</span>
                    <a href="javascript:void(0)" v-else v-on:click="page_turn(among_page + 1)">{{ among_page + 1 }}</a>
                </template>
            </template>
            <template v-else>
                <template v-if="page <= 4">
                    <template v-for="among_page in [...Array(5).keys()]">
                        <span class="thispage" v-if="page == among_page + 1">{{ among_page + 1 }}</span>
                        <a href="javascript:void(0)" v-else v-on:click="page_turn(among_page + 1)">{{ among_page + 1 }}</a>
                    </template>
                    <span class="ellipsis">······</span>
                    <a href="javascript:void(0)" v-for="among_page in [total_page-1,total_page]" v-on:click="page_turn(among_page)">{{ among_page }}</a>
                </template>
                <template v-else-if="page >= total_page - 3">
                    <a href="javascript:void(0)" v-for="among_page in [1,2]" v-on:click="page_turn(among_page)">{{ among_page }}</a>
                    <span class="ellipsis">······</span>
                    <template v-for="among_page in [...Array(5).keys()]">
                        <span class="thispage" v-if="page == total_page - 4 + among_page">{{ total_page - 4 + among_page }}</span>
                        <a href="javascript:void(0)" v-else v-on:click="page_turn(total_page - 4 + among_page)">{{ total_page - 4 + among_page }}</a>
                    </template>
                </template>
                <template v-else>
                    <a href="javascript:void(0)" v-for="among_page in [1,2]" v-on:click="page_turn(among_page)">{{ among_page }}</a>
                    <span class="ellipsis">······</span>
                    <template v-for="among_page in [...Array(5).keys()]">
                        <span class="thispage" v-if="page == page - 2 + among_page ">{{ page - 2 + among_page }}</span>
                        <a href="javascript:void(0)" v-else v-on:click="page_turn(page - 2 + among_page)">{{ page - 2 + among_page }}</a>
                    </template>
                    <span class="ellipsis">······</span>
                    <a href="javascript:void(0)" v-for="among_page in [total_page-1,total_page]" v-on:click="page_turn(among_page)">{{ among_page }}</a>
                </template>
            </template>
            <div class="input-group input-group-sm">
                <input type="text" class="form-control speech-page-swap-input" v-model="page_swap" placeholder="跳转到某页">
                <button type="submit" class="btn btn-primary speech-page-swap-button" v-on:click="page_turn(page_swap)"">跳转</button>
            </div>
        </div>
    </div>
    `
})

Vue.component("speech-popular", {
    data: function () {
        return {
            speech: null
        }
    },
    created: function () {
        this.get_speech_popular();
    },
    methods: {
        get_speech_popular: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/hotspeech/",
                withCredentials: true,
            })
            .then(function (response) {
                vm.speech = response.data.data.datalist[0];
            })
            .catch(function (error) {
                console.log(error);
            })
        },
        speech_attitude: function (attitude,textid) {
            var vm = this;
            var post_data = new URLSearchParams();
            post_data.append("attitude",attitude);
            post_data.append("textid",textid);
            axios({
                method: "post",
                url: "https://api.trickydeath.xyz/assess/",
                withCredentials: true,
                data: post_data
            })
            .then(function (response) {
                vm.$emit("refresh");
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template:`
    <div>
        <p class="main-char">热门演讲</p>
        <p class="explain" v-if="speech == null">还没有热门演讲。</p>
        <div class="speech" v-else>
            <span class="speech-avatar">
                <a v-bind:href="'people.html?uid='+speech.uid">
                    <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+speech.uid" class="img-thumbnail" width="50px" height="50px">
                </a>
                <span class="speech-content">
                    <a v-bind:href="'people.html?uid='+speech.uid">{{ speech.username }}</a>
                    <p v-html="'：'+speech.text"></p>
                </span>
            </span>
            <div class="speech-bottom">
                <p>本地演讲，第{{ speech.day }}天，{{ speech.time }}</p>
            </div>
            <div class="speech-bottom">
                <a href="javascript:void(0)" v-on:click="speech_attitude(1,speech.textid)" v-bind:class="{ 'speech-attitude' : speech.my_attitude == 1 }">欢呼({{ speech.cheer }}) </a>
                <a href="javascript:void(0)" v-on:click="speech_attitude(2,speech.textid)" v-bind:class="{ 'speech-attitude' : speech.my_attitude == 2 }">关注({{ speech.onlooker }}) </a>
                <a href="javascript:void(0)" v-on:click="speech_attitude(3,speech.textid)" v-bind:class="{ 'speech-attitude' : speech.my_attitude == 3 }">倒彩({{ speech.catcall }})</a>
            </div>
        </div>
    </div>
    `
})

Vue.component("speech-deliver", {
    data: function () {
        return {
            speech_input: "",
            speech_tips: ""
        }
    },
    methods: {
        give_speech: function () {
            var vm = this;
            var post_data = new URLSearchParams();
            post_data.append("text",this.speech_input);
            axios({
                method: "post",
                url: "https://api.trickydeath.xyz/speech/",
                withCredentials: true,
                data: post_data
            })
            .then(function (response) {
                vm.speech_tips = response.data.data.message;
                if (response.data.status == 1)
                {
                    vm.speech_input = "";
                }
                vm.$emit("refresh");
                main_vm.get_status();
            })
            .catch(function (error) {
                vm.speech_tips = response.data.data;
                console.log(error);
            })
        }
    },
    template:`
    <div class="deliver-speech">
        <p class="main-char">发表演讲</p>
        <textarea class="form-control resize-none" rows="5" id="speech-input" type="text" v-model="speech_input" placeholder="在这里发表演讲，不超过300个字"></textarea>
        <button class="btn btn-primary" v-on:click="give_speech">发表</button>
        <p class="speech-tips">{{ speech_tips }}</p>
        <p class="speech-length-tips" v-bind:class="{ 'speech-length-tips-over': speech_input.length > 300 }">{{ speech_input.length }}/300</p>
    </div>
    `
})