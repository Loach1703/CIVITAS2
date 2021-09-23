Vue.component("estate-all", {
    props: ["prop"],
    data: function () {
        return {
            estates: []
        }
    },
    created: function () {
        this.get_estate();
    },
    methods: {
        get_estate: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getestate/",
                withCredentials: true,
                params: {
                    uid: this.prop.uid,
                },
            })
            .then(function (response) {
                vm.estates = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template: `
    <div class="main-double">
        <p class="main-char">我拥有的不动产</p>
        <p class="explain">不动产不动产</p>
        <a class="btn btn-primary" href="create-estate.html">建造新的不动产</a>
        <p class="explain" v-if="estates.length == 0">你还没有不动产，点击“创建新的不动产”创建一个。</p>
    </div>
    `
})

Vue.component("estate-create", {
    props: ["prop"],
    data: function () {
        return {
            estates_list: [
                [{id:1, name:"农场"},{id:2, name:"牧场"}],
                [{id:3, name:"磨坊"},{id:4, name:"木工作坊"}],
                [{id:5, name:"住宅"},{id:6, name:"仓库"}]
            ],
            estates_type_list: [{id:0, name:"原料产出"},{id:1, name:"加工类"},{id:2, name:"住宅与设施"}],
            estate_id: -1,
            estate_type_id: -1,
            land_list: [{id:0, name:"长安县"},{id:1, name:"泥鳅县"},{id:2, name:"郊区（北）"},{id:3, name:"郊区（南）"}],
            land_type_list: [
                [{id:1,name:"平原",difficult:100,had_open_land:50,total_land:200},{id:2,name:"丘陵",difficult:400,had_open_land:50,total_land:200}],
                [{id:1,name:"平原",difficult:100,had_open_land:50,total_land:200},{id:2,name:"丘陵",difficult:400,had_open_land:50,total_land:200}],
                [{id:1,name:"平原",difficult:100,had_open_land:50,total_land:"无限"},{id:2,name:"丘陵",difficult:400,had_open_land:50,total_land:"无限"}],
                [{id:1,name:"平原",difficult:100,had_open_land:50,total_land:"无限"},{id:2,name:"丘陵",difficult:400,had_open_land:50,total_land:"无限"}]
            ],
            land_id: -1,
            land_type_id: -1
        }
    },
    created: function () {
        this.get_estate();
    },
    methods: {
        get_estate: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getestate/",
                withCredentials: true,
                params: {
                    uid: this.prop.uid,
                },
            })
            .then(function (response) {
                vm.estates = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template: `
    <div class="main-double">
        <p class="main-char">建造不动产</p>
        <p class="explain">不动产不动产</p>
        <p class="main-subchar">选择类型</p>
        <div class="estate-select-type">
            <img v-bind:src="'civitas/icon/estate/'+estate_id+'.png'" width="60px" height="60px"/>
            <div class="estate-select-single">
                <select class="form-control" v-model="estate_type_id">
                    <option disabled="disabled" value="-1">请选择不动产类型</option>
                    <option 
                        v-for="(estate_type,index) in estates_type_list" 
                        v-bind:value="estate_type.id" 
                        v-bind:key="index">
                        {{ estate_type.name }}
                    </option>
                </select>
            </div>
            <div class="estate-select-single">
                <select class="form-control" v-model="estate_id">
                    <option disabled="disabled" value="-1">请选择不动产</option>
                    <option 
                        v-for="(estate_detail,index) in estates_list[estate_type_id]" 
                        v-bind:value="estate_detail.id" 
                        v-bind:key="index">
                        {{ estate_detail.name }}
                    </option>
                </select>
            </div>
        </div>
        <p class="explain" data-toggle="collapse" data-target="#detail-message">点这里展开详细信息</p>
        <div class="collapse" id="detail-message">
            <p class="explain">不过附属建筑饼暂时没空画不过附属建筑饼暂时没空画不过附属建筑饼暂时没空画</p>
            <p class="explain">不过附属建筑饼暂时没空画不过附属建筑饼暂时没空画不过附属建筑饼暂时没空画</p>
        </div>
        <p class="main-subchar">选择建设地点</p>
        <div class="estate-select-type">
            <img v-bind:src="'civitas/icon/city/'+land_id+'.png'" width="60px" height="60px"/>
            <div class="estate-select-single">
                <select class="form-control" v-model="land_id">
                    <option disabled="disabled" value="-1">请选择土地位置</option>
                    <option 
                        v-for="(land,index) in land_list" 
                        v-bind:value="land.id" 
                        v-bind:key="index">
                        {{ land.name }}
                    </option>
                </select>
            </div>
            <div class="estate-select-single">
                <select class="form-control" v-model="land_type_id">
                    <option disabled="disabled" value="-1">请选择地形</option>
                    <option 
                        v-for="(land_type,index) in land_type_list[land_id]" 
                        v-bind:value="land_type.id" 
                        v-bind:key="index">
                        {{ land_type.name }}
                    </option>
                </select>
            </div>
        </div>
        <div class="estate-select-type" v-if="land_type_id != -1">
            <div class="estate-select-single">
                <p class="estate-location-name">开垦难度</p>
                <p class="estate-number">{{ land_type_list[land_id][land_type_id-1].difficult.toFixed(1) }}</p>
            </div>
            <div class="estate-select-single">
                <p class="estate-location-name">已开垦土地</p>
                <p class="estate-number">{{ land_type_list[land_id][land_type_id-1].had_open_land.toFixed(1) }}</p>
            </div>
            <div class="estate-select-single">
                <p class="estate-location-name">总土地数量</p>
                <p class="estate-number" v-if="land_type_list[land_id][land_type_id-1].total_land == '无限'">无限</p>
                <p class="estate-number" v-else>{{ land_type_list[land_id][land_type_id-1].total_land.toFixed(1) }}</p>
            </div>
        </div>
        <button class="btn btn-primary">建造不动产</button>
    </div>
    `
})