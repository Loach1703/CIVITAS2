/*
个人主页Vue组件

组件1
名称:people-detail
用途:个人主页中显示个人详细信息
props:{
    prop:{
        uid:对应用户的uid
        username:对应用户的用户名
    },
}
*/

Vue.component("people-detail", {
    props: ["prop","uid"],
    data: function () {
        return {
        }
    },
    created: function () {
        document.title = this.prop.username + "的主页 - 古典社会模拟 CIVITAS2";
    },
    watch: {
        prop: {
            handler: function () {
                document.title = this.prop.username + "的主页 - 古典社会模拟 CIVITAS2";
            },
            deep: true
        }
    },
    template:`
    <div class="people-detail">
        <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+prop.uid" class="img-thumbnail" width="100px" height="100px">
        <div class="people-text">
            <p>{{ prop.username }}</p>
            <p class="explain">>位于<a v-bind:href="'city.html?uid='+prop.cityid">京兆尹</a>，长安县 >籍贯<a v-bind:href="'city.html?uid='+prop.cityid">京兆尹</a></p>
            <p class="explain">><a v-bind:href="'depository.html?uid='+prop.uid">{{ prop.username }}的库房</a></p>
        </div>
        <div class="people-add-friend" v-if="prop.uid != uid">
            <button class="btn btn-sm">添加好友+</button>
        </div>
    </div>
    `
})

Vue.component("people-social", {
    props: ["prop","uid","type"],
    data: function () {
        return {
            social_types: ["公开赞扬","公开谴责","私下表扬","私下批评","赠送礼物"],
            socials: [
                {fromuid:6,touid:7,fromusername:"泥鳅养殖专家",tousername:"时间",type:0,day:105,time:"17:16:15"},
                {fromuid:6,touid:7,fromusername:"泥鳅养殖专家",tousername:"时间",type:1,day:105,time:"17:16:15"},
                {fromuid:6,touid:7,fromusername:"泥鳅养殖专家",tousername:"时间",type:0,day:105,time:"17:16:15"},
                {fromuid:6,touid:7,fromusername:"泥鳅养殖专家",tousername:"时间",type:1,day:105,time:"17:16:15"},
                {fromuid:6,touid:7,fromusername:"泥鳅养殖专家",tousername:"时间",type:0,day:105,time:"17:16:15"},
                {fromuid:6,touid:7,fromusername:"泥鳅养殖专家",tousername:"时间",type:1,day:105,time:"17:16:15"},
                {fromuid:6,touid:7,fromusername:"泥鳅养殖专家",tousername:"时间",type:0,day:105,time:"17:16:15"},
                {fromuid:6,touid:7,fromusername:"泥鳅养殖专家",tousername:"时间",type:1,day:105,time:"17:16:15"},
            ],
            length: 0
        }
    },
    created: function () {
        this.get_social();
        if (this.type == "total")
        {
            document.title = this.prop.username + "的社交记录 - 古典社会模拟 CIVITAS2"
        }
    },
    watch: {
        prop: {
            handler: function () {
                document.title = this.prop.username + "的社交记录 - 古典社会模拟 CIVITAS2";
            },
            deep: true
        }
    },
    methods: {
        get_social: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getsocial/",
                withCredentials: true,
                params: {
                    uid: this.prop.uid,
                },
            })
            .then(function (response) {
                vm.socials = response.data.data;
                if (vm.socials.length >= 5 && vm.type == 'people')
                {
                    vm.length = 5;
                }
                else
                {
                    vm.length = vm.socials.length;
                }
            })
            .catch(function (error) {
                if (vm.socials.length >= 5 && vm.type == 'people')
                {
                    vm.length = 5;
                }
                else
                {
                    vm.length = vm.socials.length;
                }
                console.log(error);
            })
        }
    },
    template:`
    <div class="social-total">
        <p class="main-char">{{ prop.username }}的社交关系</p>
        <div class="social-methods bottomline-dashed">
            <p class="explain" v-if="prop.uid == uid">你不能对自己进行社交。</p>
            <p class="explain" v-else>你还不是{{ prop.username }}的好友，但你可以<a href="javascript:void(0)">公开谴责</a>。</p>
        </div>
        <div class="social-detail">
            <p class="explain" v-if="socials.length == 0">{{ prop.username }}还没有社交记录。</p>
            <template v-else>
                <div class="social-single bottomline-dashed" v-for="(social,index) in socials.slice(0,length)" v-bind:key="index">
                    <a v-bind:href="'people.html?uid='+social.fromuid">
                        <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+social.fromuid" class="img-thumbnail" width="50px" height="50px">
                    </a>
                    <p>
                        <a v-bind:href="'people.html?uid='+social.fromuid">{{ social.fromusername }}</a> {{ social_types[social.type] }}了
                        <a v-bind:href="'people.html?uid='+social.touid">{{ social.tousername }}</a>。<br>
                        第{{ social.day }}天，{{ social.time }}。
                    </p>
                    <a v-bind:href="'people.html?uid='+social.touid">
                        <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+social.touid" class="img-thumbnail" width="50px" height="50px">
                    </a>
                </div>
            </template>
            <div class="social-more" v-if="type == 'people'">
                <a v-bind:href="'social.html?uid='+prop.uid">>>查看更多社交记录</a>
            </div>
        </div>
    </div>
    `
})