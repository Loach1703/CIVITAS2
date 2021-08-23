var recipe_vm;

function load_recipe()
{
    Vue.component('ingredient-one', {
        props: ["ingredient_list","used_ingredients","ingredient_prop","index"],
        data: function () {
            return {
                ingredient_number: "",
                ingredient_id: -1,
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
            <div class="recipe-name col-lg-2">
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
            <div class="recipe-name col-lg-2">
                <input type="number" 
                    class="form-control" 
                    v-model="ingredient_number" 
                    step="0.01"
                    placeholder="数量">
                </input>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ (ingredient_prop[ingredient_id].starvation * ingredient_number).toFixed(2) }}<br></p>
                <p class="recipe-starvation">饥饿变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ (ingredient_prop[ingredient_id].health * ingredient_number).toFixed(2) }}<br></p>
                <p class="recipe-health">健康变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ (ingredient_prop[ingredient_id].stamina * ingredient_number).toFixed(2) }}<br></p>
                <p class="recipe-stamina">精力变化</p>
            </div>
            <div class="recipe-taste">
                <p class="recipe-taste-text">味道 
                    <strong class="recipe-acid" v-if="ingredient_prop[ingredient_id].acid > 0">酸 </strong>
                    <strong class="recipe-sweet" v-if="ingredient_prop[ingredient_id].sweet > 0">甜 </strong>
                    <strong class="recipe-bitter" v-if="ingredient_prop[ingredient_id].bitter > 0">苦 </strong>
                    <strong class="recipe-salt" v-if="ingredient_prop[ingredient_id].salt > 0">咸 </strong>
                    <strong class="recipe-spice" v-if="ingredient_prop[ingredient_id].spice > 0">香料 </strong>
                    <strong class="recipe-none" v-if="ingredient_prop[ingredient_id].acid == 0 &&
                        ingredient_prop[ingredient_id].sweet == 0 &&
                        ingredient_prop[ingredient_id].bitter == 0 &&
                        ingredient_prop[ingredient_id].salt == 0 &&
                        ingredient_prop[ingredient_id].spice == 0">无 </strong>
                </p>
            </div>
            <button class="btn close float-right" v-on:click="remove_ingredients">&times;</button>
        </div>
        `
    })
    Vue.component('ingredient-total', {
        props: ["ingredient_total"],
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
        },
        watch: {
            ingredient_total: function () {
                console.log(this.ingredient_total);
            }
        },
        template: `
        <div class="recipe-total bottomline-dashed">
            <div class="recipe-total-name">
                <p>属性合计</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ starvation.toFixed(2) }}<br></p>
                <p class="recipe-starvation">饥饿变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ happiness.toFixed(2) }}<br></p>
                <p class="recipe-health">快乐变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ health.toFixed(2) }}<br></p>
                <p class="recipe-health">健康变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ stamina.toFixed(2) }}<br></p>
                <p class="recipe-stamina">精力变化</p>
            </div>
            <div class="recipe-taste">
                <p class="recipe-taste-text">味道 
                    <strong class="recipe-acid">酸 </strong>
                    <strong class="recipe-sweet">甜 </strong>
                    <strong class="recipe-bitter">苦 </strong>
                    <strong class="recipe-salt">咸 </strong>
                    <strong class="recipe-spice">香料 </strong>
                </p>
            </div>
        </div>
        `
      })
    recipe_vm = new Vue({
        el: "#main",
        data: {
            next_number: 0,
            number_of_ingredients: [],
            used_ingredients: [],
            ingredient_total: [],
            ingredient_list: [{id:6,name:"韭"},{id:7,name:"葱"},{id:8,name:"姜"},{id:14,name:"李"},{id:17,name:"桃"},{id:18,name:"甜瓜"}],
            ingredient_prop: {
                "-1":{starvation:0,health:0,stamina:0,max:5,acid:0,sweet:0,bitter:0,salt:0,spice:0},
                6:{starvation:1,health:0.05,stamina:0,max:5,acid:0,sweet:0,bitter:0,salt:0,spice:8},
                7:{starvation:1,health:0.1,stamina:0,max:5,acid:0,sweet:0,bitter:0,salt:0,spice:5},
                8:{starvation:1,health:0.2,stamina:0,max:5,acid:0,sweet:0,bitter:0,salt:0,spice:10},
                14:{starvation:1,health:0.2,stamina:0.5,max:5,acid:15,sweet:5,bitter:0,salt:0,spice:0},
                17:{starvation:1,health:0.2,stamina:0,max:5,acid:5,sweet:15,bitter:0,salt:0,spice:0},
                18:{starvation:2,health:0.2,stamina:0,max:5,acid:0,sweet:5,bitter:0,salt:0,spice:0},
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
            },
            test: function (){
                console.log(this.used_ingredients);
                console.log(this.ingredient_list);
            }
        }
    })
}