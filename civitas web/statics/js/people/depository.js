/*
仓库Vue组件

组件1
名称:depository-one
用途:显示仓库
props:{
    prop:{
    },
}
data:{
    materials:物资表
}
*/

Vue.component("depository-one", {
    props: ["prop"],
    data: function () {
        return {
            materials: []
        }
    },
    created: function () {
        var vm = this;
        axios({
            method: "get",
            url: "https://api.trickydeath.xyz/getmaterial/",
            params: {
                uid: this.prop.uid
            },
            withCredentials: true
        })
        .then(function (response) {
            vm.materials = response.data.data;
        })
        .catch(function (error) {
            console.log(error);
        })
        document.title = this.prop.username + "的库房 - 古典社会模拟 CIVITAS2";
    },
    watch: {
        prop: function () {
            document.title = this.prop.username + "的库房 - 古典社会模拟 CIVITAS2";
        }
    },
    template: `
    <div>
        <p class="main-char">{{ prop.username }}的库房</p>
        <p class="main-subchar" v-if="materials.length == 0">{{ prop.username }}还没有物品。</p>
        <div class="bottomline-dashed" v-for="material in materials" v-bind:key="material.id">
            <div class="depository-box" data-toggle="collapse" v-bind:data-target="'#material'+material.id">
                <img v-bind:src="'civitas/icon/goods/'+material.id+'.png'" width="60px" height="60px" class="depository-mainimg"/>
                <span class="depository-text1">
                    <p class="depository-name">{{ material.name }}<br></p>
                    <p class="depository-loss">仓储损耗 {{ material.wastage.toFixed(1) }}%</p>
                </span>
                <span class="depository-text2">
                    <p class="depository-num">{{ material.total.toFixed(2) }}<br></p>
                    <p class="depository-loss">总量</p>
                </span>
                <span class="depository-text2">
                    <p class="depository-num">{{ (material.total * material.unitmass).toFixed(2) }}<br></p>
                    <p class="depository-loss">每单位重量 {{ material.unitmass.toFixed(2) }}</p>
                </span>
            </div>
            <div class="depository-detail collapse" v-bind:id="'material'+material.id" v-for="detailmes in material.detail" v-bind:key="detailmes.level">
                <span class="depository-star">
                    <img v-bind:src="'civitas/icon/star/star.png'"/>
                    <img v-bind:src="'civitas/icon/star/star.png'" v-if="detailmes.level >= 2"/>
                    <img v-bind:src="'civitas/icon/star/star-none.png'" v-else/>
                    <img v-bind:src="'civitas/icon/star/star.png'" v-if="detailmes.level >= 3"/>
                    <img v-bind:src="'civitas/icon/star/star-none.png'" v-else/>
                </span>
                <span class="depository-text3">
                    <p class="depository-num">{{ detailmes.count.toFixed(2) }}<br></p>
                </span>
                <span class="depository-text3">
                    <p class="depository-num">{{ (detailmes.count * material.unitmass).toFixed(2) }}<br></p>
                </span>
            </div>
        </div>
    </div>
    `
})