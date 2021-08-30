/*
个人主页Vue组件

组件1
名称:people-detail
用途:显示演讲，翻页
props:{
    prop:{
        uid:对应用户的uid
        username:对应用户的用户名
    },
}
*/

Vue.component("people-detail", {
    props: ["prop"],
    data: function () {
        return {
            username: ""
        }
    },
    created: function () {
        this.username = this.prop.username;
        document.title = this.username + "的主页 - 古典社会模拟 CIVITAS2";
    },
    watch: {
        prop: {
            handler: function () {
                console.log(this.prop)
                this.username = this.prop.username;
                document.title = this.username + "的主页 - 古典社会模拟 CIVITAS2";
            },
            deep: true,
            immediate: true
        }
    },
    template:`
    <div class="main-people">
        <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+prop.uid" class="img-thumbnail" width="100px" height="100px">
        <div class="main-people-text">
            <p>{{ prop.test }}</p>
            <p>{{ username }}</p>
            <p class="author">&gt;位于京兆尹，长安县 &gt;籍贯京兆尹</p>
            <p class="author">&gt;<a v-bind:href="'depository.html?uid='+prop.uid">{{ username }}的库房</a></p>
        </div>
    </div>
    `
})