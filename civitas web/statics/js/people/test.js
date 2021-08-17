var main;
var app;

function abc()
{
  Vue.component("depository-a", {
    props: ["material"],
    template: `
      <div class="depository-box bottomline-dashed">
        <img v-bind:src="'https://api.trickydeath.xyz/getavatar/?uid='+material.id" width="60px" height="60px" class="depository-mainimg"/>
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
          <p class="depository-loss">每单位重量 {{ material.unitmass }}</p>
        </span>
        <p>{{ material.id }}</p>
        <button class="btn btn-primary" v-on:click="$emit('remove')">remove</button>
      </div>
    `
  })
  app = new Vue({
    el: "#app",
    data: {
      next_id: 1,
      materials: [
        { id: 0, name: "小麦",total: 100,unitmass: 10 }
      ]
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
            day: this.day_html,
            city: this.city_html
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