/*
获取库房信息
load_depository：获得库房信息
*/

var depository_vm;

function load_depository(uid)
{
    Vue.component("depository-one", {
        props: ["material"],
        template: `
        <div class="bottomline-dashed">
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
        `
      })
      depository_vm = new Vue({
        el: "#main",
        data: {
          materials: []
        },
        created: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getmaterial/",
                params: {
                    uid: uid
                },
                withCredentials: true
            })
            .then(function (response) {
                var json_str_data = response.data.data;
                vm.materials = json_str_data;
            })
            .catch(function (error) {
                console.log(error);
                document.getElementById("depository-name").innerHTML = "找不到该用户！"
            })
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getuserdetail/",
                params: {
                    uid: uid
                },
                withCredentials: true
            })
            .then(function (response) {
                var json_str_data = response.data.data;
                document.title = json_str_data.username + "的库房 - 古典社会模拟 CIVITAS2";
                document.getElementById("depository-name").innerHTML = json_str_data.username + "的库房";
                try
                {
                    document.getElementById("depository-none").innerHTML = json_str_data.username + "还没有物品。";
                }
                catch (e){}
            })
            .catch(function (error) {
                console.log(error);
                document.getElementById("depository-name").innerHTML = "找不到该用户！"
            })
        },
        methods: {
        }
      })
}