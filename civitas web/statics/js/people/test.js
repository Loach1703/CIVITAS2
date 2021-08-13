var app;

function abc()
{
  Vue.component("depository", {
    props: ["material"],
    template: `
      <div class="depository-box bottomline-dashed">
        <img v-bind:src="material.id" width="60px" height="60px" class="depository-mainimg"/>
        <span class="depository-text1">
          <p class="depository-name">{{ material.name }}<br></p>
          <p class="depository-loss">仓储损耗 10%</p>
        </span>
        <span class="depository-text2">
          <p class="depository-num">{{ material.total }}<br></p>
          <p class="depository-loss">总量</p>
        </span>
        <span class="depository-text2">
          <p class="depository-num">{{ material.total * material.unitmass }}<br></p>
          <p class=\"depository-loss\">每单位重量 {{ material.unitmass }}</p>
        </span>
      </div>
    `
  })
  var app = new Vue({
    el: "#app",
    data: {
      materials: [
        { id: 1, name: "小麦",total: 100,unitmass: 10 },
        { id: 6, name: "大麦",total: 200,unitmass: 5 },
        { id: 7, name: "粟",total: 300,unitmass: 1 }
      ]
    }
  })
  var main_right = new Vue({
    el: "#mainright",
    data: {
      speech_input: ""
    }
  })
}

window.onload = abc