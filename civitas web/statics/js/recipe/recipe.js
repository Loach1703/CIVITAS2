/*
食谱部分Vue组件

组件1
名称:ingredient-detail
用途:创建/编辑食谱时，显示食谱材料详细信息
props:{
    ingredient_list: 食材总表
    used_ingredients: 已使用的食材
    ingredient_prop: 各个食材属性
    index: 材料编号
}
*/

Vue.component("ingredient-detail", {
    props: ["ingredient_list","used_ingredients","ingredient_prop","index"],
    data: function () {
        return {
            ingredient_number: "",
            ingredient_id: -1,
            ingredient_quality: 1
        }
    },
    methods: {
        ingredient_change: function () {
            if (this.ingredient_id == -1) 
            {
                return
            }
            this.$emit("ingredient_change",this.index,this.ingredient_id,this.ingredient_number);
        },
        remove_ingredients: function () {
            this.$emit("remove", this.index);
        }
    },
    watch: {
        ingredient_id: function () {
            this.ingredient_change();
        },
        ingredient_number: function (value,old_value) {
            if (isNaN(value))
            {
                this.ingredient_number = old_value;
            }
            if (value < 0)
            {
                this.ingredient_number = 0;
            }
            else if (value > this.ingredient_prop[this.ingredient_id].max)
            {
                this.ingredient_number = this.ingredient_prop[this.ingredient_id].max;
            }
            this.ingredient_number = this.ingredient_number = Math.round(this.ingredient_number * 100) / 100;
            this.ingredient_change();
        }
    },
    template: `
    <div class="recipe-single bottomline-dashed">
        <img v-bind:src="'civitas/icon/goods/'+ingredient_id+'.png'" class="float-left" width="60px" height="60px"/>
        <div class="recipe-select">
            <select class="form-control" v-model="ingredient_id">
                <option disabled="disabled" value="-1">请选择</option>
                <option 
                    v-for="(ingredient_mes,index) in ingredient_list" 
                    v-bind:disabled="used_ingredients.includes(ingredient_mes.id)"
                    v-bind:value="ingredient_mes.id" 
                    v-bind:key="index">
                    {{ ingredient_mes.name }}
                </option>
            </select>
        </div>
        <div class="recipe-select">
            <input type="number" 
                class="form-control" 
                v-model="ingredient_number" 
                step="0.01"
                placeholder="数量">
            </input>
        </div>
        <div class="recipe-select">
            <select class="form-control" v-model="ingredient_quality">
                <option value="1">Q1</option>
                <option value="2">Q2</option>
                <option value="3">Q3</option>
            </select>
        </div>
        <div class="recipe-prop">
            <p class="recipe-number">{{ (ingredient_prop[ingredient_id].starvation * ingredient_number).toFixed(2) }}<br></p>
            <p class="recipe-prop-single">饥饿变化</p>
        </div>
        <div class="recipe-prop">
            <p class="recipe-number">{{ (ingredient_prop[ingredient_id].health * ingredient_number).toFixed(2) }}<br></p>
            <p class="recipe-prop-single">健康变化</p>
        </div>
        <div class="recipe-prop">
            <p class="recipe-number">{{ (ingredient_prop[ingredient_id].stamina * ingredient_number).toFixed(2) }}<br></p>
            <p class="recipe-prop-single">精力变化</p>
        </div>
        <div class="recipe-taste">
            <p class="recipe-taste-text">味道 
                <strong class="recipe-acid" v-if="ingredient_prop[ingredient_id].acid > 0">酸 </strong>
                <strong class="recipe-sweet" v-if="ingredient_prop[ingredient_id].sweet > 0">甜 </strong>
                <strong class="recipe-bitter" v-if="ingredient_prop[ingredient_id].bitter > 0">苦 </strong>
                <strong class="recipe-salt" v-if="ingredient_prop[ingredient_id].salt > 0">咸 </strong>
                <strong class="recipe-spice" v-if="ingredient_prop[ingredient_id].spice > 0">香 </strong>
                <strong class="recipe-none" v-if="ingredient_prop[ingredient_id].acid == 0 &&
                    ingredient_prop[ingredient_id].sweet == 0 &&
                    ingredient_prop[ingredient_id].bitter == 0 &&
                    ingredient_prop[ingredient_id].salt == 0 &&
                    ingredient_prop[ingredient_id].spice == 0">无 
                </strong>
            </p>
        </div>
        <button class="btn close" v-on:click="remove_ingredients">&times;</button>
    </div>
    `
})

Vue.component("ingredient-total", {
    props: ["ingredient_total","type"],
    data: function () {
        return {
            starvation: 0,
            happiness: 0,
            health: 0,
            stamina: 0,
            acid: 0,
            sweet: 0,
            bitter: 0,
            salt: 0,
            spice: 0
        }
    },
    methods: {
        get_total_props: function () {
        }
    },
    watch: {
        ingredient_total: function () {
            this.get_total_props();
        }
    },
    template: `
    <div>
        <p class="recipe-total-name" v-if="type == 'create'">属性合计</p>
        <div class="recipe-single bottomline-dashed">
            <p class="recipe-name" v-if="type == 'myrecipe'">{{ ingredient_total.name }}</p>
            <div class="recipe-prop">
                <p class="recipe-number">{{ starvation.toFixed(2) }}<br></p>
                <p class="recipe-prop-single">饥饿变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ happiness.toFixed(2) }}<br></p>
                <p class="recipe-prop-single">快乐变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ health.toFixed(2) }}<br></p>
                <p class="recipe-prop-single">健康变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ stamina.toFixed(2) }}<br></p>
                <p class="recipe-prop-single">精力变化</p>
            </div>
            <div class="recipe-taste">
                <p class="recipe-taste-text">味道 
                    <strong class="recipe-acid" v-if="acid > 0">酸 </strong>
                    <strong class="recipe-sweet" v-if="sweet > 0">甜 </strong>
                    <strong class="recipe-bitter" v-if="bitter > 0">苦 </strong>
                    <strong class="recipe-salt" v-if="salt > 0">咸 </strong>
                    <strong class="recipe-spice" v-if="spice > 0">香料 </strong>
                    <strong class="recipe-none" v-if="acid == 0 && sweet == 0 && bitter == 0 && salt == 0 && spice == 0">无 </strong>
                </p>
            </div>
        </div>
    </div>
    `
    })

Vue.component('ingredient-all', {
    data: function () {
        return {
            next_number: 0,
            number_of_ingredients: [],
            used_ingredients: [],
            ingredient_total: [],
            ingredient_list: [{id:6,name:"韭"},{id:7,name:"葱"},{id:8,name:"姜"},{id:14,name:"李"},{id:17,name:"桃"},{id:18,name:"甜瓜"}],
            ingredient_prop: {
                "-1":{starvation:0,health:0,stamina:0,acid:0,sweet:0,bitter:0,salt:0,spice:0},
                6:{starvation:1,health:0.05,stamina:0,acid:0,sweet:0,bitter:0,salt:0,spice:8},
                7:{starvation:1,health:0.1,stamina:0,acid:0,sweet:0,bitter:0,salt:0,spice:5},
                8:{starvation:1,health:0.2,stamina:0,acid:0,sweet:0,bitter:0,salt:0,spice:10},
                14:{starvation:1,health:0.2,stamina:0.5,acid:15,sweet:5,bitter:0,salt:0,spice:0},
                17:{starvation:1,health:0.2,stamina:0,acid:5,sweet:15,bitter:0,salt:0,spice:0},
                18:{starvation:2,health:0.2,stamina:0,acid:0,sweet:5,bitter:0,salt:0,spice:0},
            }
        }
    },
    created: function () {
        this.add_ingredients();
    },
    methods: {
        add_ingredients: function (){
            this.number_of_ingredients.push(this.next_number);
            this.used_ingredients.push({id:-1,number:0});
            this.ingredient_total.push({id:-1,number:0});
            this.next_number++;
        },
        remove_ingredients: function (index){
            this.number_of_ingredients.splice(index, 1);
            this.used_ingredients.splice(index, 1);
            this.ingredient_total.splice(index, 1);
            this.next_number--;
        },
        ingredients_had_changed: function (index,ingredient_id,ingredient_number){
            this.$set(this.used_ingredients,index,ingredient_id)
            this.$set(this.ingredient_total,index,{id:ingredient_id,number:ingredient_number})
        }
    },
    template: `
    <div class="main-double">
        <p class="main-char">新建食谱</p>
        <p class="author">创建全新的食谱以供享用。</p>
        <input type="text" class="form-control" placeholder="食谱名"></input>
        <button class="btn btn-success">保存食谱</button>
        <button class="btn btn-warning">取消</button>
        <ingredient-detail 
            v-for="(ingredient_id,index) in number_of_ingredients"  
            v-on:remove="remove_ingredients" 
            v-on:ingredient_change="ingredients_had_changed"
            v-bind:ingredient_list="ingredient_list" 
            v-bind:used_ingredients="used_ingredients" 
            v-bind:ingredient_prop="ingredient_prop" 
            v-bind:index="index" 
            v-bind:key="ingredient_id">
        </ingredient-detail>
        <button class="btn btn-success" v-on:click="add_ingredients">添加食材</button>
        <ingredient-total v-bind:ingredient_total="ingredient_total" v-bind:type="'create'"></ingredient-total>
    </div>
    `
})

Vue.component('recipe-all', {
    props: ["prop"],
    data: function () {
        return {
            recipes: []
        }
    },
    created: function () {
        this.get_recipe();
    },
    methods: {
        get_recipe: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getrecipe/",
                withCredentials: true,
                params: {
                    uid: this.prop.uid,
                },
            })
            .then(function (response) {
                vm.recipes = response.data.data;
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template: `
    <div class="main-double">
        <p class="main-char">我的食谱</p>
        <a class="btn btn-primary" href="create_recipe.html" role="button">新建食谱</a>
        <p class="author" v-if="recipes.length == 0">你还没有食谱，点击“新建食谱”创建一个。</p>
        <ingredient-total v-else v-for="(recipe,index) in recipes" v-bind:key="index" v-bind:ingredient_total="recipe" v-bind:type="'myrecipe'"></ingredient-total>
    </div>
    `
})