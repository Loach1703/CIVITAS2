/*
天气Vue组件

组件1
名称:weather-detail
用途:显示天气
props:{
    prop:{
    },
    city:城市天气
}
data:{
    weather_svg_dict:天气图标
}
*/

Vue.component("weather-detail", {
    props: ["prop","city"],
    data: function () {
        return {
            weather_svg_dict: {"晴":"qingtian.svg","多云":"duoyun.svg","阴":"yintian.svg","小雨":"xiaoyu.svg","大雨":"dayu.svg","小雪":"xiaoxue.svg","大雪":"daxue.svg","台风":"taifeng.svg"},
            weather: "",
            temperature: 0.0,
            rain_num: 0.0,
            day: 0
        }
    },
    created: function () {
        this.get_weather();
    },
    watch: {
        prop: function () {
            this.get_weather();
        }
    },
    methods: {
        get_weather: function () {
            var vm = this;
            axios({
                method: "get",
                url: "https://api.trickydeath.xyz/getweather/",
                withCredentials: true,
                params: {
                    city: this.city,
                    day: this.prop.total_day
                },
            })
            .then(function (response) {
                vm.weather = response.data.data.weather;
                vm.temperature = response.data.data.temperature;
                vm.rain_num = response.data.data.rain_num;
                vm.day = response.data.data.day;
            })
            .catch(function (error) {
                console.log(error);
            })
        }
    },
    template:`
    <div>
        <p class="location">位于京兆尹，长安县 今天是{{ prop.season }}的第{{ day }}天</p>
        <img v-bind:src="'civitas/svg/weather/'+weather_svg_dict[weather]"/>
        <p class="weather-main">今日天气：<strong>{{ weather }}</strong> 温度：<strong>{{ temperature.toFixed(2) }}</strong>摄氏度 降水量：<strong>{{ rain_num.toFixed(2) }}</strong>mm</p>
    </div>
    `
})