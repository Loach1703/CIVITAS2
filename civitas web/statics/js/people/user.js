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
    props: ["prop"],
    data: function () {
        return {
        }
    },
    created: function () {
        document.title = this.prop.username + "的主页 - 古典社会模拟 CIVITAS2";
    },
    watch: {
        prop: {
            handler: function (val,oldVal) {
                console.log(this.prop)
                console.log(val)
                console.log(oldVal)
                document.title = this.prop.username + "的主页 - 古典社会模拟 CIVITAS2";
            },
            deep: true
        }
    },
    template:`
    <div class="main-people">
        <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+prop.uid" class="img-thumbnail" width="100px" height="100px">
        <div class="main-people-text">
            <p>{{ prop.test }}</p>
            <p>{{ prop.username }}</p>
            <p class="explain">>位于<a v-bind:href="'city.html?uid='+prop.cityid">京兆尹</a>，长安县 >籍贯<a v-bind:href="'city.html?uid='+prop.cityid">京兆尹</a></p>
            <p class="explain">><a v-bind:href="'depository.html?uid='+prop.uid">{{ prop.username }}的库房</a></p>
        </div>
    </div>
    `
})