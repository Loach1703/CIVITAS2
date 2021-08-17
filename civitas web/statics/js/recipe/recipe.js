function recipe_vm()
{
    Vue.component('ingredient', {
        props: ["prop"],
        template: `
        <div class="recipe-single bottomline-dashed">
            <img src="civitas/icon/goods/1.png" class="float-left" width="60px" height="60px"/>
            <div class="recipe-name col-lg-2">
                <select class="form-control">
                    <option disabled value="0">请选择</option>
                    <option value="1">小麦粉</option>
                    <option value="2">桃</option>
                    <option value="3">野菜</option>
                </select>
            </div>
            <div class="recipe-name col-lg-2">
                <input type="text" class="form-control" v-model="prop.recipe_number" placeholder="数量"></input>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ (prop.recipe_prop.starvation * prop.recipe_number).toFixed(2) }}<br></p>
                <p class="recipe-starvation">饥饿变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ (prop.recipe_prop.health * prop.recipe_number).toFixed(2) }}<br></p>
                <p class="recipe-health">健康变化</p>
            </div>
            <div class="recipe-prop">
                <p class="recipe-number">{{ (prop.recipe_prop.stamina * prop.recipe_number).toFixed(2) }}<br></p>
                <p class="recipe-stamina">精力变化</p>
            </div>
            <div class="recipe-taste">
                <p class="recipe-taste-text">味道 <strong class="recipe-acid">酸 </strong><strong class="recipe-sweet">甜 </strong><strong class="recipe-bitter">苦 </strong><strong class="recipe-salt">咸 </strong></p>
            </div>
        </div>
        `
      })
    var vm = new Vue({
        el: "#recipe-inner",
        data: {
            prop: {
                recipe_prop: { starvation: 10, health: 1, stamina: 10},
                recipe_number: 0
            },
        },
        methods: {
            add_ingredients: function (){
            }
        }
    })
}