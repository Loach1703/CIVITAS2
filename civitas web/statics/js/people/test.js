var main;
var app;

function abc()
{
  var day_html = 1;
  var city_html = "长安";
  Vue.component("depository-a", {
    props: ["material"],
    template: `
    <div>
      <div class="depository-box bottomline-dashed" data-toggle="collapse" v-bind:data-target="'#material'+material.id">
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
        <p>{{ material.id }}</p>
        <button class="btn btn-primary" v-on:click="$emit('remove')">remove</button>
      </div>
      <div class="depository-detail bottomline-dashed collapse" v-bind:id="'material'+material.id" v-for="detailmes in material.detail">
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
  app = new Vue({
    el: "#app",
    data: {
      next_id: 1,
      materials: [{"id": 1, "name": "\u5c0f\u9ea6", "unitmass": 0, "wastage": 0, "total": 13.187532813624408, "detail": [{"level": 1, "count": 13.187532813624408}]}, {"id": 6, "name": "\u97ed", "unitmass": 0, "wastage": 0, "total": 19.27316022089894, "detail": [{"level": 1, "count": 19.27316022089894}]}, {"id": 8, "name": "\u59dc", "unitmass": 0, "wastage": 0, "total": 2.9021805676817496, "detail": [{"level": 1, "count": 2.9021805676817496}]}, {"id": 20, "name": "\u91ce\u83dc", "unitmass": 0, "wastage": 0, "total": 16.42911805354969, "detail": [{"level": 1, "count": 16.42911805354969}]}, {"id": 23, "name": "\u79bd\u8089", "unitmass": 0, "wastage": 0, "total": 0.7584000000000001, "detail": [{"level": 1, "count": 0.7584000000000001}]}, {"id": 27, "name": "\u5c0f\u9ea6\u7c89", "unitmass": 0, "wastage": 0, "total": 6.0, "detail": [{"level": 1, "count": 1.0}, {"level": 2, "count": 2.0}, {"level": 3, "count": 3.0}]}, {"id": 36, "name": "\u539f\u6728", "unitmass": 0, "wastage": 0, "total": 35.62549444986179, "detail": [{"level": 1, "count": 35.62549444986179}]}]
    },
    methods: {
      get_get: function () {
        this.materials.push({ id: this.next_id, name: "大麦", total: this.next_id*100, unitmass: this.next_id*2 });
        this.next_id++;
      }
    }
  })
  main = new Vue({
    el: "#main",
    data: {
      day_html: "",
      city_html: "",
      weather: "",
      season: "",
      day: "",
      rain: "",
      temperature: "",
      speech_input: ""
    },
    methods: {
      get_weather: function () {
        axios({
          method: "get",
          url: "https://api.trickydeath.xyz/getweather/",
          params: {
            day: day_html,
            city: city_html
          }
        })
        .then(function (response) {
          main.$data.weather = response.data["data"]["weather"];
          main.$data.season = response.data["data"]["season"];
          main.$data.day = response.data["data"]["day"];
          main.$data.rain = response.data["data"]["rain_num"];
          main.$data.temperature = response.data["data"]["temperature"].toFixed(2);
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      sideline: function () {
        axios({
          method: "post",
          url: "https://api.trickydeath.xyz/dosideline/",
          withCredentials: true,
          data: {
              sidelineid: this.day_html,
              typeid: this.city_html
          },
        })
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
      }
    }
  })
}

window.onload = abc