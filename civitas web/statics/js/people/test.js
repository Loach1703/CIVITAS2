var main_vm;

function abc() {
  main_vm = new Vue({
    el: "#main",
    data: {
      prop: {
        title:"好啊",
        statement:"太好了",
        type:"work_strategy",
        option_text:["好","你好","挺好的","不错","可以","还行","大胜","牛啊","确实","咋了"]
      }
    },
    methods: {
      show_ranevent_modal: function () {
        $("#ranevent").modal("show");
      },
      hide_ranevent_modal: function () {
        $("#ranevent").modal("hide");
      },
      get_ranevent: function (url) {
        var vm = this;
        axios({
          method: "get",
          url: url,
          withCredentials: true,
        })
        .then(function (response) {
          var json_str_data = response.data.data;
          vm.prop = json_str_data.ranevent_data;
        })
        .catch(function (error) {
          console.log(error);
        });
      }
    }
  })
}

window.onload = abc

Vue.component("ranevent-modal", {
  props: ["prop"],
  methods: {
    hide_modal: function (){
      this.$emit("hide_modal");
    },
    next_modal: function (url){
      this.$emit("hide_modal");
      this.$emit("next_modal",url);
    }
  },
  template:`
  <div class="modal fade" id="ranevent" aria-hidden="true">
      <div class="modal-dialog">
          <div class="modal-content modal-background">
              <div class="modal-body bottomline-dashed">
                <p class="modal-title-text">{{ prop.title }}</p>
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
              </div>
              <div class="modal-body bottomline-dashed">
                  <p>{{ prop.statement }}</p>
              </div>
              <div class="modal-body ranevent-option" v-if="prop.type == 'work_strategy'">
                  <button 
                    type="button" 
                    class="btn" 
                    v-on:click="hide_modal" 
                    v-for="index in [...Array(prop.option_text.length).keys()]">
                    <img v-bind:src="'civitas/icon/work/Strategy_'+index+'.png'"/>
                    {{ prop.option_text[index] }}
                  </button>
              </div>
              <div class="modal-body ranevent-option" v-else>
                  <button 
                    type="button" 
                    class="btn" 
                    v-on:click="hide_modal" 
                    v-for="index in [...Array(prop.option_text.length).keys()]">
                    <img v-bind:src="'civitas/icon/choices/Choice_'+index+'.png'"/>
                    {{ prop.option_text[index] }}
                  </button>
              </div>
          </div>
      </div>
  </div>
  `
})
Vue.component("great-vue", {
  template:`
  <p class="main-char">我的CIVITAS</p>
  `
})